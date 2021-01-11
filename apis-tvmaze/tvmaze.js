/** Given a query string, return array of matching shows:
 *     { id, name, summary, episodesUrl }
 */

/** Search Shows
 *    - given a search term, search for tv shows that
 *      match that query.  The function is async show it
 *       will be returning a promise.
 *
 *   - Returns an array of objects. Each object should include
 *     following show information:
 *    {
        id: <show id>,
        name: <show name>,
        summary: <show summary>,
        image: <an image from the show data, or a default imege if no image exists, (image isn't needed until later)>
      }
 */
async function searchShows(query) {
  const shows = [];
  query = checkSpacing(query);
  const url = `http://api.tvmaze.com/search/shows?q=${query}`;
  const res = await axios.get(url).then(function (response) {
    return response.data;
  });

  for (let obj of res) {
    let img = "";
    if (obj.show.image !== null) {
      img = obj.show.image.original;
    } else {
      img = "https://tinyurl.com/tv-missing";
    }
    const showObj = {
      id: obj.show.id,
      name: obj.show.name,
      image: img,
      summary: obj.show.summary,
    };
    shows.push(showObj);
  }
  return shows;
}

/** Takes the query string and puts it in to proper syntax for the API request */
function checkSpacing(str) {
  const notPermitted = "'!?;.,<>@#$/";
  let fixedStr = "";
  for (let char of str) {
    if (!notPermitted.includes(char)) {
      if (char === " ") {
        fixedStr = fixedStr + "-";
      } else {
        fixedStr = fixedStr + char;
      }
    }
  }
  return fixedStr;
}

/** Populate shows list:
 *     - given list of shows, add shows to DOM
 */

function populateShows(shows) {
  const $showsList = $("#shows-list");
  $showsList.empty();

  for (let show of shows) {
    let $item = $(
      `<div class="col-md-6 col-lg-3 Show" data-show-id="${show.id}">
         <div class="card" data-show-id="${show.id}">
         <img class="card-img-top" src="${show.image}">
           <div class="card-body">
             <h5 class="card-title">${show.name}</h5>
             <p class="card-text">${show.summary}</p>
             <button class="btn btn-block btn-success episodeBtn" data-show-id="${show.id}">Episodes</button>
           </div>
         </div>
       </div>
      `
    );

    $showsList.append($item);
  }
}

/** Handle search form submission:
 *    - hide episodes area
 *    - get list of matching shows and show in shows list
 *    - empties the search form
 */

$("#search-form").on("submit", async function handleSearch(evt) {
  evt.preventDefault();

  let query = $("#search-query").val();
  if (!query) return;
  $("#search-form").val("");
  $("#episodes-area").hide();

  let shows = await searchShows(query);

  populateShows(shows);
});

/**Handles click on an "Episodes" button:
 *    - get show ID
 *    - get the episodes list from the API
 *    - populate the episodes list
 */

$("#shows-list").on("click", "button", async function (evt) {
  const showId = evt.target.dataset.showId;
  let episodes = await getEpisodes(showId);
  populateEpisodes(episodes);
});

/** Given a show ID, return list of episodes:
 *      { id, name, season, number }
 */

async function getEpisodes(id) {
  const episodes = [];
  const res = await axios
    .get(`http://api.tvmaze.com/shows/${id}/episodes`)
    .then(function (response) {
      return response.data;
    });

  for (let episode of res) {
    let episodeObj = {
      id: episode.id,
      name: episode.name,
      season: episode.season,
      number: episode.number,
    };
    episodes.push(episodeObj);
  }
  return episodes;
}

/**Takes an array of episode objects, creates the LI's, adds them to the list, then displays the episodes area */

function populateEpisodes(episodes) {
  const $episodesList = $("#episodes-list");
  $episodesList.empty();

  for (let episode of episodes) {
    let $item = $(
      `<li>${episode.name} (Season ${episode.season}, Number ${episode.number})</li>`
    );

    $episodesList.append($item);
  }
  $("#episodes-area").show();
}
