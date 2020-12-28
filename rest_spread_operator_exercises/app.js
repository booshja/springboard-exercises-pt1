const filterOutOdds = (...args) => nums.filter((num) => num % 2 === 0);

const findMin = (...args) => Math.min(...args);

const mergeObjects = (obj1, obj2) => ({ ...obj1, ...obj2 });

const doubleAndReturnArgs = (arr, ...args) => [
  ...arr,
  ...args.map((val) => val * 2),
];

const removeRandom = (...items) => {
  const removed = Math.floor(Math.random() * Math.floor(items.length));
  return [...items.slice(0, removed), ...items.slice(removed + 1)];
};

const extend = (array1, array2) => {
  [...array1, ...array2];
};

const addKeyVal = (obj, key, val) => {
  let newObj = { ...obj };
  newObj[key] = val;
  return newObj;
};

const removeKey = (obj, key) => {
  let newObj = { ...obj };
  delete newObj[key];
  return newObj;
};

/** Combine two objects and return a new object. */

const combine = (obj1, obj2) => ({ ...obj1, ...obj2 });

const update = (obj, key, val) => ({ ...obj, [key]: val });
