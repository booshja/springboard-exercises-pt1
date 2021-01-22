function findUserByUsername(usersArray, username) {
  return usersArray.find(function (user) {
    return user.username === username;
  });
}

function removeUser(usersArray, username) {
  let found = usersArray.findIndex(function (user) {
    return user.username === username;
  });

  if (found === -1) return;

  return usersArray.splice(found, 1)[0];
}
