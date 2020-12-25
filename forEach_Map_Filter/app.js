const numbers = [1, 2, 3, 5, 10, 22];
const words = ["colt", "matt", "tim", "test", "hi", "goodbye", "smile"];
const keyValArray = [
  { name: "Elie" },
  { name: "Tim" },
  { name: "Matt" },
  { name: "Colt" },
];
const fullName = [
  { first: "Elie", last: "Schoppik" },
  { first: "Tim", last: "Garcia" },
  { first: "Matt", last: "Lane" },
  { first: "Colt", last: "Steele" },
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

// Write a function called extractKey which accepts an array of objects and some key and returns a new array with the value of that key in each object.
function extractKey(keyValArray, key) {
  return keyValArray.map(function (value) {
    return value[key];
  });
}

// Write a function called extractFullName which accepts an array of objects and returns a new array with the value of the key with a name of “first” and the value of a key with the name of “last” in each object, concatenated together with a space.
function extractFullName(fullName) {
  return fullName.map(function (person) {
    return person["first"] + " " + person["last"];
  });
}

//START OF FILTER
// Write a function called filterByValue which accepts an array of objects and a key and returns a new array with all the objects that contain that key.
function filterByValue() {}

// Write a function called find which accepts an array and a value and returns the first element in the array that has the same value as the second parameter or undefined if the value is not found in the array.
function find() {}

// Write a function called findInObj which accepts an array of objects, a key, and some value to search for and returns the first found value in the array.
function findInObj() {}

//Write a function called removeVowels which accepts a string and returns a new string with all of the vowels (both uppercased and lowercased) removed. Every character in the new string should be lowercased.
function removeVowels() {}

// Write a function called doubleOddNumbers which accepts an array and returns a new array with all of the odd numbers doubled (HINT - you can use map and fitler to double and then filter the odd numbers).
function doubleOddNumbers() {}
