import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList

class TextGenerator:
    def __init__(self, model_name, **kwargs):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, **kwargs)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", output_attentions=True, **kwargs)

    def generate_text(self, input_text, max_new_tokens=100, stop_newline=True):
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
        if stop_newline:
            stopping_criteria = StoppingCriteriaList([StopOnNewLineCriteria(self.tokenizer)])
        else:
            stopping_criteria = None
        outputs = self.model.generate(input_ids, max_new_tokens=max_new_tokens, output_attentions=True, return_dict_in_generate=True, stopping_criteria=stopping_criteria)
        generated_text = self.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        attentions = outputs.attentions
        return generated_text, attentions, self.tokenizer, input_ids, outputs

class StopOnNewLineCriteria(StoppingCriteria):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def __call__(self, input_ids, scores, **kwargs):
        # 마지막으로 생성된 토큰이 줄바꿈인지 확인
        if input_ids[0, -1] == self.tokenizer.eos_token_id or \
            self.tokenizer.decode(input_ids[0, -1]) == "\n":
            return True
        return False

class InterSentenceAttention:
    def __init__(self, generated_text, generated_sequences, attentions, tokenizer):
        self.tokenizer = tokenizer

        # 문장을 마침표 기준으로 분리
        # sentences = [sentence.strip() for sentence in generated_text.split('\n') if sentence.strip()]
        sentence_boundaries, sentences = self._find_sentence_boundaries(generated_sequences)

        # 문장 간 attention 계산
        integrated_attentions = self._integrate_attentions(attentions)
        sentence_attention_heads = self._calculate_sentence_attention(integrated_attentions, sentence_boundaries)
        sentence_attention = self._aggregate_attention(sentence_attention_heads)

        self.sentences = sentences
        self.sentence_attention_heads = sentence_attention_heads
        self.sentence_attention = sentence_attention

    
    def _integrate_attentions(self, attentions):
        num_layers = len(attentions)
        _, num_heads, prompt_seq_length, _ = attentions[0][-1].shape
        max_seq_length = attentions[-1][-1].shape[-1]

        integrated = torch.zeros((1, num_heads, max_seq_length, max_seq_length))
        integrated[0, :, :prompt_seq_length, :prompt_seq_length] = attentions[0][-1] # 0번째 레이어(프롬프트 간의 attention을 가짐)의 마지막 히든 레이어의 heads들은 그대로 붙임
        # 나머지 레이어들(생성된 토큰들과 이전 토큰들의 attention을 가짐)의 마지막 히든 레이어의 heads들을 이어붙임
        for layer in range(1, num_layers):
            integrated[0, :, prompt_seq_length+layer:prompt_seq_length+layer+1, :prompt_seq_length+layer] = attentions[layer][-1][0]
        
        return integrated # shape: (1, num_heads, max_seq_length, max_seq_length)
    
    def _aggregate_attention(self, sentence_attentions):
        # input shape: (1, num_heads, num_sentences, num_sentences)
        print(sentence_attentions.shape)
        max_attention_heads, _ = torch.max(sentence_attentions, dim=1)
        print(max_attention_heads.shape)

        return max_attention_heads.squeeze(0) # shape: (num_sentences, num_sentences)

    def _find_sentence_boundaries(self, sequences):
        boundaries = [0]
        sentences = []

        for i, token in enumerate(sequences):
            decoded = self.tokenizer.decode(token)
            if '\n' in decoded:
                sentences.append(self.tokenizer.decode(sequences[boundaries[-1]:i]))
                boundaries.append(i)

        sentences.append(self.tokenizer.decode(sequences[boundaries[-1]:len(sequences)]))
        boundaries.append(len(sequences))

        return boundaries, sentences

    def _calculate_sentence_attention(self, attentions, sentence_boundaries):
        # 문장 간 attention 계산
        # num_layers = len(attentions)
        # num_layers = 1
        _, num_heads, _, seq_length = attentions.shape # shape: (1, num_heads, seq_length, seq_length)
        num_sentences = len(sentence_boundaries) - 1 # 시작점과 끝점을 포함하므로 1 뺌
        print(sentence_boundaries)

        # 0으로 초기화
        sentence_attentions = torch.zeros((1, num_heads, num_sentences, num_sentences))

        # for layer in range(num_layers):
        # layer = 0
        for head in range(num_heads):
            for i in range(num_sentences):
                start_i = sentence_boundaries[i]
                end_i = sentence_boundaries[i + 1]
                for j in range(num_sentences):
                    start_j = sentence_boundaries[j]
                    end_j = sentence_boundaries[j + 1]
                    # 문장 범위 내 텐서 추출
                    attention_slice = attentions[0, head, start_i:end_i, start_j:end_j]
                    
                    if attention_slice.numel() == 0: # 빈 텐서 검사
                        max_attention = 0
                    else:
                        max_attention = torch.max(attention_slice).item() # 문장 내 토큰들의 attention의 최대값
                    
                    sentence_attentions[0, head, i, j] = max_attention # 각 헤드 내에서 i번째 문장관 j번째 문장의 attention

        return sentence_attentions # shape: (1, num_heads, num_sentences, num_sentences)
