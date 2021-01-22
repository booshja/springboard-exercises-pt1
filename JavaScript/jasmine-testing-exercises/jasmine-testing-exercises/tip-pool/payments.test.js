describe("payments tests", function () {
  beforeEach(function () {
    billAmtInput.value = 100;
    tipAmtInput.value = 30;
  });

  it("should add a new payment on submit", function () {
    submitPaymentInfo();
    expect(Object.keys(allPayments).length).toEqual(1);
    expect(allPayments["payment1"].billAmt).toEqual("100");
    expect(allPayments["payment1"].tipAmt).toEqual("30");
    expect(allPayments["payment1"].tipPercent).toEqual(30);
  });

  it("shouldn't add a new payment on blank submit", function () {
    billAmtInput.value = "";
    tipAmtInput.value = "";
    submitPaymentInfo();
    expect(Object.keys(allPayments).length).toEqual(0);
  });

  it("createCurPayment() shouldn't return a value when billAmt or tipAmt is empty", function () {
    billAmtInput.value = "";
    submitPaymentInfo();
    expect(createCurPayment()).not.toBeDefined();

    billAmtInput.value = "100";
    tipAmtInput.value = "";
    submitPaymentInfo();
    expect(createCurPayment()).not.toBeDefined();
  });

  it("createCurPayment() should create a new payment", function () {
    let expected = { billAmt: "100", tipAmt: "30", tipPercent: 30 };
    expect(createCurPayment()).toEqual(expected);
  });

  it("appendPaymentTable() should add another tr & td's", function () {
    let payment = createCurPayment();
    allPayments["payment1"] = payment;

    appendPaymentTable(payment);

    let tdList = document.querySelectorAll("#paymentTable tbody tr td");

    expect(tdList.length).toEqual(4);
    expect(tdList[0].innerText).toEqual("$100");
    expect(tdList[1].innerText).toEqual("$30");
    expect(tdList[2].innerText).toEqual("30%");
    expect(tdList[3].innerText).toEqual("X");
  });

  afterEach(function () {
    billAmtInput.value = "";
    tipAmtInput.value = "";
    paymentTbody.innerHTML = "";
    summaryTds[0].innerHTML = "";
    summaryTds[1].innerHTML = "";
    summaryTds[2].innerHTML = "";
    serverTbody.innerHTML = "";
    paymentId = 0;
    allPayments = {};
  });
});
