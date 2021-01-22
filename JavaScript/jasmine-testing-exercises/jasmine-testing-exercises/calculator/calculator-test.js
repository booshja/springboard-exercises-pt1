beforeAll(function () {});

it("should calculate the monthly rate correctly", function () {
  expect(
    calculateMonthlyPayment({ amount: 10000, years: 5, rate: 3.62 })
  ).toEqual("182.46");
});

it("should return a result with 2 decimal places", function () {
  expect(
    calculateMonthlyPayment({ amount: 10055, years: 10, rate: 3.62 })
  ).toEqual("100.00");
});

it("should handle a really big loan correctly", function () {
  expect(
    calculateMonthlyPayment({ amount: 1500000, years: 7, rate: 4.56 })
  ).toEqual("20892.13");
});

it("should handle a really high interest rate", function () {
  expect(
    calculateMonthlyPayment({ amount: 1500, years: 7, rate: 89.24 })
  ).toEqual("111.82");
});
