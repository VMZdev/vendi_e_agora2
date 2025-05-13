from datetime import datetime
from src.views.http_types.http_response import HttpResponse
from src.views.http_types.http_request import HttpRequest
import logging
logger = logging.getLogger(__name__)

class UploadController:
    def __init__(self, repository):
        self.__repository = repository

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            if not http_request or not hasattr(http_request, 'method'):
                logger.error("Requisição inválida")
                return HttpResponse(
                    status_code=400,
                    body={"error": "Requisição inválida"}
                )
            
            if http_request.method == "GET":
                return self._get_upload_history()
            elif http_request.method == "POST":
                return self._process_upload(http_request)
            else:
                return HttpResponse(
                    status_code=405,
                    body={"error": "Método não permitido"}
                )
                
        except Exception as e:
            logger.error(f"Erro no controller: {str(e)}", exc_info=True)
            return HttpResponse(
                status_code=500,
                body={"error": "Erro interno no servidor"}
            )

    def _get_upload_history(self) -> HttpResponse:
        try:
            uploads = self.__repository.get_upload_history()
            return HttpResponse(
                status_code=200,
                body={"uploads": uploads}
            )
        except Exception as e:
            logger.error(f"Erro ao buscar histórico: {str(e)}")
            return HttpResponse(
                status_code=500,
                body={"error": "Falha ao buscar histórico de uploads"}
            )

    def _process_upload(self, http_request: HttpRequest) -> HttpResponse:
        try:
            if not hasattr(http_request, 'files') or not http_request.files.get('files'):
                return HttpResponse(
                    status_code=400,
                    body={"error": "Nenhum arquivo fornecido"}
                )

            results = []
            errors = []
            
            for file in http_request.files['files']:
                if not file.filename:
                    continue

                try:
                    file.seek(0)  # Reset file pointer
                    file_content = file.read()
                    
                    if not file_content:
                        raise ValueError("Arquivo está vazio")

                    processing_results = self.__repository.process_excel_data(file)
                    
                    upload_id = self.__repository.add_upload_record(
                        filename=file.filename,
                        file_size=len(file_content),
                        file_type=file.filename.split('.')[-1].lower()
                    )
                    
                    results.append({
                        "id": upload_id,
                        "name": file.filename,
                        "size": f"{len(file_content)/1024:.2f} KB",
                        "results": processing_results
                    })

                except Exception as e:
                    errors.append(f"{file.filename}: {str(e)}")
                    continue
                finally:
                    file.seek(0)

            response_body = {
                "message": f"Processado {len(results)} arquivo(s), {len(errors)} erro(s)",
                "processed_files": results,
                "errors": errors if errors else None
            }

            if results:
                response_body["stats"] = {
                    'total_customers': sum(r['results']['customers_saved'] for r in results),
                    'total_products': sum(r['results']['products_saved'] for r in results),
                    'total_sales': sum(r['results']['sales_saved'] for r in results)
                }

            return HttpResponse(
                status_code=200 if results else 400 if errors else 500,
                body=response_body
            )
            
        except Exception as e:
            logger.error(f"Erro no processamento: {str(e)}", exc_info=True)
            return HttpResponse(
                status_code=500,
                body={"error": "Falha no processamento"}
            )