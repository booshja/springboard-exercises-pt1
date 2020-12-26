function extractValue(arr, key) {
  return arr.reduce(function (acc, nextObj) {
    acc.push(nextObj[key]);
    return acc;
  }, []);
}

function vowelCount(str) {
  const vowels = "aeiou";
  return str.split("").reduce(function (accum, nextLetter) {
    let lowerCase = nextLetter.toLowerCase();
    if (vowels.indexOf(lowerCase) !== -1) {
      if (accum[lowerCase]) {
        accum[lowerCase]++;
      } else {
        accum[lowerCase] = 1;
      }
    }
    return accum;
  }, {});
}

function addKeyAndValue(arr, key, value) {
  return arr.reduce(function (accum, nextObj, idx) {
    accum[idx][key] = value;
    return accum;
  }, arr);
}

function partition(arr, callback) {
  return arr.reduce(
    function (acc, next) {
      if (callback(next)) {
        acc[0].push(next);
      } else {
        acc[1].push(next);
      }
      return acc;
    }[([], [])]
  );
}
