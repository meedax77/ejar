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
      <div class="payment-form">
        <label for="id_payment_date_${formIndex}">Payment Date</label>
        <input type="date" name="payment_date_${formIndex}" id="id_payment_date_${formIndex}">
        <label for="id_payment_amount_${formIndex}">Payment Amount</label>
        <input type="number" name="payment_amount_${formIndex}" id="id_payment_amount_${formIndex}">
      </div>
    `;
    const formElement = $(formHtml);
    paymentFormsContainer.append(formElement);
  }

  startDateInput.addEventListener('change', calculateNumberOfDays);
  endDateInput.addEventListener('change', calculateNumberOfDays);
  addPaymentButton.addEventListener('click', addPaymentForm);
});