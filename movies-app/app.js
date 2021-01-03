$("#submit").click(function (event) {
  event.preventDefault();
  const title = $("#movie-title").val();
  const rating = $("#movie-rating").val();
  const movieItem = $("<li>")
    .text("Movie: " + title + " Rating: " + rating + "/10  ")
    .append("<button class='removeBtn'>Remove</button>");
  $("#ratings-list").append(movieItem);
  $("input").val("");
});

//TODO: ADD EVENT LISTENER FOR REMOVING LI'S
$("#ratings-list").on("click", "li button", function (e) {
  $(this).parent().remove();
});
