from fastapi import HTTPException
import time
import json
from datetime import datetime
from dataclasses import dataclass
from src.domain.usecase.repository.search import AbstractSearchRepository
from src.domain.usecase.embedding.search import AbstractSearchEmbedding
from src.domain.usecase.io_usecase.search import SearchUseCaseInput, SearchUseCaseOutput
from src.domain.usecase.guardrails.search import AbstractSearchGuardrails

@dataclass
class SearchUseCase:
    search_repository: AbstractSearchRepository
    search_embedding: AbstractSearchEmbedding
    search_guardrails: AbstractSearchGuardrails

    async def execute(self, input: SearchUseCaseInput) -> SearchUseCaseOutput:
        try:
            request_start = time.perf_counter()
            timestamp = datetime.utcnow().isoformat() + "Z"
            if not self.search_guardrails.sanitize(message=input.message):
                raise HTTPException(
                    status_code=403,
                    detail="Política violada: a solicitação contém conteúdo proibido."
                )

            vector = self.search_embedding.generate_vector(target=input.message)

            retrieval_start = time.perf_counter()
            response = await self.search_repository.find_similarity(vector=vector, limit=3, with_payload=True)
            retrieval_end = time.perf_counter()

            if not response:
                answer_text = "Não encontrei informações suficientes para responder com precisão."
                return SearchUseCaseOutput(
                    answer=answer_text,
                    citations=[],
                    metrics={}
                )

            best_score = response[0].score
            if best_score < 0.3:
                answer_text = "Não encontrei informações suficientes para responder com precisão."
                return SearchUseCaseOutput(
                    answer=answer_text,
                    citations=[],
                    metrics={}
                )
            if response:
                knowledge_base = ""
                citations_set = set()
                top_k = len(response) if response else 0

                for target in response:
                    knowledge_base += "\n" + target.payload.get("text", {})
                    title = target.payload.get("title", "")
                    
                    if title:
                        citations_set.add(title)

                answer_text = f"""
                Você é um assistente especializado em responder perguntas com base **exclusivamente** na base de conhecimento fornecida abaixo.  
                Use **somente essas informações** para gerar a resposta.

                ### OBJETIVOS
                1. Produza uma resposta clara, objetiva e correta.
                2. Todas as afirmações devem estar **ancoradas nas fontes** presentes na base de conhecimento.
                3. Sempre utilize **citações** para justificar cada parte relevante da resposta.
                4. Se a base de conhecimento não contiver informação suficiente, diga explicitamente:
                "Não encontrei informações suficientes para responder com precisão."

                ### COMO RESPONDER
                - Utilize **somente** informações presentes na base.
                - Não invente ou assuma nada que não esteja citado.
                - Utilize o formato de citação assim:
                    - (Fonte: TÍTULO DA FONTE)
                - Utilize quantas citações forem necessárias.
                - Seja direto e didático.

                ### BASE DE CONHECIMENTO
                    {knowledge_base}

                ### FONTES DISPONÍVEIS
                    {citations_set}

                Agora gere a melhor resposta possível, sempre fundamentada nas fontes acima.
                """
                request_end = time.perf_counter()

                latencia_total_ms = round((request_end - request_start) * 1000)
                latencia_retrieval_ms = round((retrieval_end - retrieval_start) * 1000)
                estimativa_tokens_prompt = round(len(input.message) / 4)
                estimativa_tokens_response = round(len(answer_text) / 4)
                total_tokens = estimativa_tokens_prompt + estimativa_tokens_response

                metrics = {
                    "latencia_total_ms": latencia_total_ms,
                    "latencia_retrieval_ms": latencia_retrieval_ms,
                    "estimativa_tokens": total_tokens
                }
                log_entry = {
                    "timestamp": timestamp,
                    "latencia_total_ms": latencia_total_ms,
                    "latencia_retrieval_ms": latencia_retrieval_ms,
                    "estimativa_tokens_prompt": estimativa_tokens_prompt,
                    "estimativa_tokens_response": estimativa_tokens_response,
                    "estimativa_tokens": total_tokens,
                    "top_k": top_k,
                    "tamanho_contexto": len(knowledge_base),
                    "citations": list(citations_set)
                }

                print(json.dumps(log_entry, ensure_ascii=False))

                return SearchUseCaseOutput(answer=answer_text, citations=list(citations_set), metrics=metrics)

        except Exception as e:
            print(e)
            return e