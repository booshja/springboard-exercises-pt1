const api_key = "BUwYvWo6SBuu7pifo3d7PWWm4ubFENYq";
const limit = 1;

$("#submit").on("click", function (e) {
  e.preventDefault();
  const term = $("#gifInput").val();
  const url = getGiphy(term);
});

$("#clearBtn").on("click", function (e) {
  $("#imgRow").html("");
});

async function getGiphy(term) {
  const q = term;
  const offset = Math.floor(Math.random() * 100);
  try {
    const res = await axios.get("https://api.giphy.com/v1/gifs/search", {
      params: { q, api_key, limit, offset },
    });
    const url = res.data.data[0].images.fixed_height.url;
    $("<img>")
      .attr({ src: url })
      .addClass("img-fluid")
      .appendTo($("<div>").addClass("col-4").appendTo($("#imgRow")));
    $("#gifInput").val("");
  } catch {
    $("#gifInput").val("");
    alert("That didn't seem to work! Try another search term.");
  }
}
