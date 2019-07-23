let update_preview = () => {
  let top_line = document.querySelector('#new_meme_preview .line1');
  let middle_line = document.querySelector('#new_meme_preview .line2');
  let bottom_line = document.querySelector('#new_meme_preview .line3')
  let image = document.querySelector('#new_meme_preview img');
  top_line.innerHTML = document.querySelector("#top_text_input").value;
  middle_line.innerHTML = document.querySelector("#middle_text_input").value;
  bottom_line.innerHTML = document.querySelector("#bottom_text_input").value;
  image.src = document.querySelector('input[name="image"]:checked+label img').src
};

document.querySelectorAll("#new_meme_form input").forEach(
  (el) => {el.addEventListener("change", update_preview)});
