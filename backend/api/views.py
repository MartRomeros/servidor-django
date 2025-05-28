import io
from django.http import FileResponse,JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from openpyxl import Workbook
from xhtml2pdf import pisa
import json
from django.template.loader import render_to_string

@api_view(['POST'])
def exportar_archivo(request):
    tipo = request.data.get("tipo")
    data = request.data.get("data")

    if not tipo or not data:
        return JsonResponse({"error": "Faltan campos requeridos."}, status=400)

    if tipo == "excel":
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte"

        # Encabezados
        ws.append(["Nombre", "Apellido", "RUN", "Monto Acumulado"])
        ws.append([data["nombre"], data["apellido"], data["run"], data["montoacumulado"]])

        ws.append([])
        ws.append(["Actividad", "Horas"])
        for actividad in data["horasrealizadas"]:
            ws.append([actividad["actividad"], actividad["horas"]])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return FileResponse(
            output,
            as_attachment=True,
            filename="reporte.xlsx",
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    elif tipo == "pdf":
        html_string = render_to_string("reporte_pdf.html", {"data": data})
        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.StringIO(html_string), dest=result)

        if pisa_status.err:
            return HttpResponse("Error al generar el PDF", status=500)

        result.seek(0)
        return FileResponse(
            result,
            content_type='application/pdf',
            as_attachment=True,
            filename='reporte.pdf'
        )

    else:
        return JsonResponse({"error": "Tipo de archivo no válido (pdf o excel)."}, status=400)



