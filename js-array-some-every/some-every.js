var arr = [
  { title: "Instructor", first: "Elie", last: "Schoppik" },
  { title: "Instructor", first: "Tim", last: "Garcia", isCatOwner: true },
  { title: "Instructor", first: "Matt", last: "Lane" },
  { title: "Instructor", first: "Colt", last: "Steele", isCatOwner: true },
];

function hasOddNumber(arr) {
  return arr.some(function (num) {
    return num % 2 !== 0;
  });
}

function hasAZero(num) {
  return num
    .toString()
    .split("")
    .some(function (num) {
      return num === "0";
    });
}

function hasOnlyOddNumbers(arr) {
  return arr.every(function (num) {
    return num % 2 !== 0;
  });
}

function hasNoDuplicates(arr) {
  return arr.every(function (val) {
    return arr.indexOf(val) === arr.lastIndexOf(val);
  });
}

function hasCertainKey(arr, key) {
  return arr.every(function (val) {
    return key in val;
  });
}

function hasCertainValue(arr, key, searchValue) {
  return arr.every(function (val) {
    return val[key] === searchValue;
  });
}
