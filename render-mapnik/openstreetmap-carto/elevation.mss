#srtm-10 {
  [zoom >= 14][zoom < 19] {
    line-width: 0.5;
    line-color: #9cb197;
  }
}

#srtm-50 {
  [zoom >= 12][zoom < 14] {
    line-width: 0.9;
    line-color: #9cb197;
  }
  [zoom >= 14][zoom < 19] {
    line-width: 0.9;
    line-color: #9cb197;
    text-name: "[height]";
    text-size: 8;
    text-fill: #9cb197;
    text-face-name: @book-fonts;
    text-halo-radius: 1;
    text-placement: line;
  }
}

#srtm-100 {
  [zoom >= 11][zoom < 12] {
    line-width: 1.3;
    line-color: #9cb197;
  }
  [zoom >= 12][zoom < 14] {
    line-width: 1.3;
    line-color: #9cb197;
    text-name: "[height]";
    text-size: 8;
    text-fill: #9cb197;
    text-face-name: @book-fonts;
    text-halo-radius: 1;
    text-placement: line;
  }
  [zoom >= 14][zoom < 19] {
    line-width: 1.3;
    line-color: #9cb197;
    text-name: "[height]";
    text-size: 8;
    text-fill: #9cb197;
    text-face-name: @book-fonts;
    text-halo-radius: 1;
    text-placement: line;
  }
}

