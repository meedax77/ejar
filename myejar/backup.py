from django.db.models import F
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

'''
def payment_received(request, contract_id, payment_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    payment = get_object_or_404(Payment, id=payment_id, contract=contract)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            if payment.amount is None:
                payment.amount = Decimal(0)
            # use update_or_create to update the existing payment record
            payment, created = Payment.objects.update_or_create(
                id=payment.id,
                defaults={
                    'received_amount': payment.received_amount,
                    'received_date': payment.received_date,
                    'payment_method': payment.payment_method,
                    # use F expression to subtract the received amount from the amount
                    'amount': F('amount') - payment.received_amount
                }
            )
            payment.save()
            buffer = io.BytesIO()
            # create the PDF object, using the buffer as its "file"
            p = canvas.Canvas(buffer, pagesize=letter)
            # set the font and size
            p.setFont("Helvetica", 12)
            # draw the title
            p.drawCentredString(4.25 * inch, 10 * inch, " سند القبض")
            # draw a line
            p.line(0.5 * inch, 9.75 * inch, 8 * inch, 9.75 * inch)
            # draw the contract information
            p.drawString(0.5 * inch, 9.25 * inch, f"Contract Number: {contract.contractNumber}")
            p.drawString(0.5 * inch, 8.75 * inch, f"Contract Date: {contract.startDate}")
            p.drawString(0.5 * inch, 8.25 * inch, f"Contract Amount: {contract.payment_amount}")
            # draw the payment information
            p.drawString(4.5 * inch, 8.75 * inch, f"Payment Date: {payment.received_date}")
            p.drawString(4.5 * inch, 8.25 * inch, f"Payment Amount: {payment.received_amount}")
            p.drawString(4.5 * inch, 7.75 * inch, f"Payment Method: {payment.payment_method}")
            # draw a thank you message
            p.drawCentredString(4.25 * inch, 7 * inch, "Thank you for your payment!")
            # close the PDF object cleanly, and we're done
            p.showPage()
            p.save()
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file
            buffer.seek(0)
            return  FileResponse(buffer, as_attachment=True, filename=f"payment_{payment.received_amount}.pdf") 
    else:
        form = PaymentForm(instance=payment)
    
    context = {
        'contract': contract,
        'form': form,
    }
    return render(request, 'payment_received.html', context)3
    '''