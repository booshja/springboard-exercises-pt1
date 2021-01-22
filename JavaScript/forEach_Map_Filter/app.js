const numbers = [1, 2, 3, 5, 10, 22, 1, 1];
const words = ["colt", "matt", "tim", "test", "hi", "goodbye", "smile"];
const keyValArray = [
  { name: "Elie" },
  { name: "Tim" },
  { name: "Matt" },
  { name: "Colt" },
];
const fullName = [
  { first: "Elie", last: "Schoppik" },
  { first: "Tim", last: "Garcia", isDogOwner: true },
  { first: "Matt", last: "Lane" },
  { first: "Colt", last: "Steele", isDogOwner: true },
];

function doubleValues(numbers) {
  let doubled = [];

  numbers.forEach(function (num) {
    doubled.push(num * 2);
  });

  return doubled;
}

function onlyEvenValues(numbers) {
  let evens = [];

  numbers.forEach(function (num) {
    if (num % 2 === 0) {
      evens.push(num);
    }
  });

  return evens;
}

function showFirstAndLast(words) {
  let firstAndLast = [];

  words.forEach(function (letter) {
    firstAndLast.push(letter[0] + letter.slice(-1));
  });

  return firstAndLast;
}

function addKeyValue(keyValArray, key, value) {
  let keyValsUpdated = [];

  keyValArray.forEach(function (obj) {
    obj[key] = value;
    keyValsUpdated.push(obj);
  });

  return keyValsUpdated;
}

function vowelCount(fullString) {
  const vowels = "aeiou";
  splitString = fullString.split("");
  let vowelCount = {};

  splitString.forEach(function (letter) {
    let lowerCaseLetter = letter.toLowerCase();
    if (vowels.includes(lowerCaseLetter)) {
      if (vowelCount[lowerCaseLetter]) {
        vowelCount[lowerCaseLetter]++;
      } else {
        vowelCount[lowerCaseLetter] = 1;
      }
    }
  });
  return vowelCount;
}

function doubleValuesWithMap(numbers) {
  const mapDoubles = numbers.map(function (num) {
    return num * 2;
  });
  return mapDoubles;
}

function valTimesIndex(numbers) {
  const valXIndex = numbers.map(function (num, index) {
    return num * index;
  });
  return valXIndex;
}

function extractKey(keyValArray, key) {
  return keyValArray.map(function (value) {
    return value[key];
  });
}

function extractFullName(fullName) {
  return fullName.map(function (person) {
    return person["first"] + " " + person["last"];
  });
}

function filterByValue(fullName, key) {
  return fullName.filter(function (first) {
    return first[key] !== undefined;
  });
}

function find(numbers, value) {
  let found = numbers.filter(function (num) {
    return num === value;
  });
  if (found.length > 0) {
    return found[0];
  }
}

function findInObj(array, key, value) {
  return (found = array.filter(function (obj) {
    return obj[key] === value;
  })[0]);
}

function removeVowels(string) {
  const vowels = "aeiou";
  return string
    .toLowerCase()
    .split("")
    .filter(function (letter) {
      return vowels.indexOf(letter) === -1;
    })
    .join("");
}

function doubleOddNumbers(arr) {
  return arr
    .filter(function (val) {
      return val % 2 !== 0;
    })
    .map(function (val) {
      return val * 2;
    });
}
