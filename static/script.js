
// set base url for API - makes it easier to change for the whole document
const BASE_URL = "/api/cupcakes"


// On document load
$(document).ready(async function () {

  let response = await axios.get(BASE_URL);
  let data = response.data.cupcakes;

  for ({size, image, rating, flavor} of data) {
    $('#cupcake-list').append(`
      <li>
        <img class="cupcake" src="${image}"> rating: ${rating} size: ${size} flavor: ${flavor}
      </li>
    `)
  }

  $('#cupcake').on('submit', async function (e) {
    e.preventDefault();
    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = Number($('#rating').val());
    let image = $('#image').val();
    await axios.post(BASE_URL, {
      flavor,
      size,
      rating,
      image
    });

    $('#cupcake-list').append(`
      <li>
        <img class="cupcake" src="${image}"> rating: ${rating} size: ${size} flavor: ${flavor}
      </li>
    `)
  });
});