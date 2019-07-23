function new_element(tag_name, attributes, children=[]){
  let el = document.createElement(tag_name)
  for (let attr in attributes){
    el.setAttribute(attr, attributes[attr]);
  }
  for (let child in children){
    el.appendChild(children[child]);
  }
  return el
}

function insert_meme(desc){
  let new_div = new_element('div', {'class': 'meme-div'}, [
    new_element('img', {'src': 'meme_images/' + desc['image_file']}),
    new_element('h2', {'class': 'line1'}, [document.createTextNode(desc['top_text'])]),
    new_element('h2', {'class': 'line2'}, [document.createTextNode(desc['middle_text'])]),
    new_element('h2', {'class': 'line3'}, [document.createTextNode(desc['bottom_text'])]),
  ]);
  let container = document.querySelector("#memes_container");
  container.insertBefore(new_div, container.children[0]);
}

function refresh_memes() {

  fetch('/updated_memes?after=' + latest_meme_key , {'credentials': 'include'} )
    .then((data) => {return data.json()})
    .then((json) => {
      if (json.length > 0){
        latest_meme_key = json[0].key;
      }
      for (let i in json) {
        insert_meme(json[i]);
      }
    })
}


setInterval(refresh_memes, 3000)
