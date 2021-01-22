// Checks the data, and then creates a new LI with a remove button with the input
$("#submit").click(function (event) {
  event.preventDefault();
  // Checking the data: at least 2 chars in title, rating is a number and between 0-10,
  if ($("#movie-title").val().length() > 1) {
    if (typeof +$("#movie-rating").val() === "number") {
      if ($("#movie-rating").val() >= 0 && $("#movie-rating").val() <= 10) {
        const title = $("#movie-title").val();
        const rating = $("#movie-rating").val();
        const movieItem = $("<li>")
          .text("Movie: " + title + " Rating: " + rating + "/10  ")
          .append("<button class='removeBtn'>Remove</button>");
        $("#ratings-list").append(movieItem);
        $("input").val("");
      } else {
        alert("Error: Your rating must be a number between 0 and 10!");
      }
    } else {
      alert("Error: Your rating must be a number!");
    }
  } else {
    alert("Error: Your movie title must be at least 2 characters long.");
  }
});

// Listener for the remove buttons in the list
$("#ratings-list").on("click", "li button", function () {
  $(this).parent().remove();
});
