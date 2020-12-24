describe("helpers tests", function () {
  beforeEach(function () {
    billAmtInput.value = 100;
    tipAmtInput.value = 30;
    submitPaymentInfo();

    it("should sum the total of tipAmt", function () {
      expect(sumPaymentTotal("tipAmt")).toEqual(30);

      billAmtInput.value = 183.75;
      tipAmtInput.value = 40.43;
      submitPaymentInfo();

      expect(sumPaymentTotal("tipAmt")).toEqual(70.43);
    });

    it("should sum the total of billAmt", function () {
      expect(sumPaymentTotal("billAmt")).toEqual(100);

      billAmtInput.value = 183.75;
      tipAmtInput.value = 40.43;
      submitPaymentInfo();

      expect(sumPaymentTotal("billAmt")).toEqual(283.75);
    });

    it("should sum the total of tipPercent", function () {
      expect(sumPaymentTotal("tipPercent")).toEqual(30);

      billAmtInput.value = 183.75;
      tipAmtInput.value = 40.43;
      submitPaymentInfo();

      expect(sumPaymentTotal("tipPercent")).toEqual(52);
    });

    it("should calculate the tip percent", function () {
      expect(calculateTipPercent(100, 30)).toEqual(30);
      expect(calculateTipPercent(183.75, 40.43)).toEqual(22);
    });

    it("should append a new td", function () {
      let newTr = document.createElement("tr");
      appendDeleteBtn(newTr);
      expect(newTr.children.length).toEqual(1);
      expect(newTr.firstChild.innerHTML).toEqual("X");
    });

    afterEach(function () {
      billAmtInput.value = "";
      tipAmtInput.value = "";
      paymentTbody.innerHTML = "";
      summaryTds[0].innerHTML = "";
      summaryTds[1].innerHTML = "";
      serverTbody.innerHTML = "";
      allPayments = {};
      paymentId = 0;
    });
  });
});
