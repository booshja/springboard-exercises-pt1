window.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("calc-form");
  if (form) {
    setupIntialValues();
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      update();
    });
  }
});

function getCurrentUIValues() {
  return {
    amount: +document.getElementById("loan-amount").value,
    years: +document.getElementById("loan-years").value,
    rate: +document.getElementById("loan-rate").value,
  };
}

// Get the inputs from the DOM.
// Put some default values in the inputs
// Call a function to calculate the current monthly payment
function setupIntialValues() {
  values = getCurrentUIValues();
  document.getElementById("loan-amount").placeholder = "10000";
  document.getElementById("loan-years").placeholder = "5";
  document.getElementById("loan-rate").placeholder = "3.62";
  update();
}

// Get the current values from the UI
// Update the monthly payment
function update() {
  values = getCurrentUIValues();
  updateMonthly(calculateMonthlyPayment(values));
}

// Given an object of values (a value has amount, years and rate ),
// calculate the monthly payment.  The output should be a string
// that always has 2 decimal places.
function calculateMonthlyPayment(values) {
  const p = values["amount"];
  const n = Math.floor(values["years"] * 12);
  const i = values["rate"] / 100 / 12;
  const numerator = p * i;
  const denominator = 1 - Math.pow(1 + i, -1 * n);
  if (numerator === 0 || denominator === 0) {
    console.log("zero test");
    return "0.00";
  } else {
    const payment = numerator / denominator;
    const paymentString = payment.toFixed(2);
    console.log("payment: ", paymentString);
    return paymentString;
  }
}

// Given a string representing the monthly payment value,
// update the UI to show the value.
function updateMonthly(monthly) {
  const monthlyPayment = document.getElementById("monthly-payment");
  monthlyPayment.innerText = "$" + monthly;
}
