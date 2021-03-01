async function get_cupcakes() {
  /**
   * Get the cupcake data from the server
   * Create a list and append to the DOM
   */
  const cupcakes = await axios.get("/api/cupcakes").then(function (res) {
    return res.data;
  });
  for (let i = 0; i < cupcakes.cupcakes.length; i++) {
    $(
      `<li id=${cupcakes.cupcakes[i].flavor}>${cupcakes.cupcakes[i].flavor}</li>`
    ).appendTo("#cupcakes-list");
  }
}

$("#cake-form").on("submit", async function (evt) {
  /**
   * Get all the data from the form
   * Convert data to a JSON object
   * Send to the server
   * Append the new cupcake to the list on the DOM
   */
  evt.preventDefault();
  const flavor = $("#flavor").val();
  const size = $("#size").val();
  const rating = $("#rating").val();
  const image = $("#image").val();

  const json_cup = {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image,
  };

  await axios.post("api/cupcakes", json_cup);

  $(`<li id=${flavor}>${flavor}</li>`).appendTo("#cupcakes-list");
});

$(document).ready(get_cupcakes);
