$(document).ready(function() {
    const startDateInput = document.getElementById('id_startDate');
    const endDateInput = document.getElementById('id_endDate');
    const numberOfDaysInput = document.getElementById('numberOfDays');
    const paymentFormsContainer = document.getElementById('payment-forms');
    const addPaymentButton = document.querySelector('.add-payment-button');
  
    function calculateNumberOfDays() {
      const startDate = new Date(startDateInput.value);
      const endDate = new Date(endDateInput.value);
      const timeDiff = endDate.getTime() - startDate.getTime();
      const numberOfDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
      numberOfDaysInput.value = numberOfDays.toString();
    }
  
    function addPaymentForm() {
      const formIndex = paymentFormsContainer.querySelectorAll('.payment-form').length;
      const formPrefix = `payment-${formIndex}`;
      const formHtml = `
      <div id="payment-forms">
      {% for form in payment_formset %}
        {{ form }}
      {% endfor %}
    </div>
      `;
      const formElement = $(formHtml);
      formElement.find(':input').each(function () {
        const name = $(this).attr('name').replace('empty', formIndex);
        $(this).attr('name', name);
        $(this).attr('id', `id_${name}`);
      });
      paymentFormsContainer.append(formElement);
    }
  
    startDateInput.addEventListener('change', calculateNumberOfDays);
    endDateInput.addEventListener('change', calculateNumberOfDays);
    addPaymentButton.addEventListener('click', addPaymentForm);
  });