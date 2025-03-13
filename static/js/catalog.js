function toggle(imgId, exercisesId) {
    var imageElement = document.getElementById(imgId);
    var exercisesElement = document.getElementById(exercisesId);
    if (imageElement.style.display == "none") {
      imageElement.style.display = "block";
      exercisesElement.style.display = "block";
    } else {
      imageElement.style.display = "none";
      exercisesElement.style.display = "none";
    }
  }
  
  function toggleFavorite(imgElement) {
    var favoriteImg = imgElement.getAttribute('data-favorite-src');
    var nonFavoriteImg = imgElement.getAttribute('data-nonfavorite-src');
  
    if (imgElement.src.includes('nonfavorite.png')) {
      imgElement.src = favoriteImg;
      favoriteExercise.update.one;
    } else {
      imgElement.src = nonFavoriteImg;
      favoriteExercise.update,one;
    }
  }