const api_key = "BUwYvWo6SBuu7pifo3d7PWWm4ubFENYq";
const limit = 1;

console.log("Let's get this party started!");

$("#submit").on("click", function (e) {
  e.preventDefault();
  const term = $("#gifInput").val();
  getGiphy(term);
});

async function getGiphy(term) {
  const q = term;
  try {
    const res = await axios.get("https://api.giphy.com/v1/gifs/search", {
      params: {
        q,
        api_key,
        limit,
      },
    });
    console.log(res);
  } catch {
    console.log("oopsie");
  }
}
