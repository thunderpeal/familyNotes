/* Special thanks to Hung Nguyen and his medium article */
function makeResizableDiv(div) {
  const elem = document.querySelector(div);
  const resizer = document.querySelector(div + ' .resizer')
  const minimum_size = 20;
  let original_width = 0;
  let original_height = 0;
  let original_x = 0;
  let original_y = 0;
  let original_mouse_x = 0;
  let original_mouse_y = 0;

  resizer.addEventListener('mousedown', function(e) {
      e.preventDefault()
      original_width = parseFloat(getComputedStyle(elem, null).getPropertyValue('width').replace('px', ''));
      original_height = parseFloat(getComputedStyle(elem, null).getPropertyValue('height').replace('px', ''));
      original_x = elem.getBoundingClientRect().left;
      original_y = elem.getBoundingClientRect().top;
      original_mouse_x = e.pageX;
      original_mouse_y = e.pageY;
      window.addEventListener('mousemove', resize)
      window.addEventListener('mouseup', stopResize)
    })

    function resize(e) {
      const width = original_width + (e.pageX - original_mouse_x);
      const height = original_height + (e.pageY - original_mouse_y);
      if (width > minimum_size) {
        elem.style.width = width + 'px'
      }
      if (height > minimum_size) {
        elem.style.height = height + 'px'
      }
    }

    function stopResize() {
      window.removeEventListener('mousemove', resize)
    }
}

makeResizableDiv('.resizable')