// accepts 'tipAmt', 'billAmt', 'tipPercent' and sums total from allPayments objects
function sumPaymentTotal(type) {
  let total = 0;

  for (let key in allPayments) {
    let payment = allPayments[key];

    total += Number(payment[type]);
  }
  return total;
}

// converts the bill and tip amount into a tip percent
function calculateTipPercent(billAmt, tipAmt) {
  return Math.round(100 / (billAmt / tipAmt));
}

// expects a table row element, appends a newly created td element from the value
function appendTd(tr, value) {
  let newTd = document.createElement("td");
  newTd.innerText = value;

  tr.append(newTd);
}

// expects a table row element, appends a newly created td element from the value
function appendDeleteBtn(tr) {
  let newDelBtn = document.createElement("td");
  newDelBtn.className = "deleteBtn";
  newDelBtn.innerText = "X";
  newDelBtn.addEventListener("click", deleteLine);

  tr.append(newDelBtn);
}

function deleteLine(e) {
  let ele = e.target.closest("tr");

  delete allServers[ele.id];
  delete allPayments[ele.id];

  ele.parentNode.removeChild(ele);
  updateServerTable();
  updateSummary();
}
