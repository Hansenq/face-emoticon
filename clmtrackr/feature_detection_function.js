// Import these
// <script src="./js/utils.js"></script>
// <script src="./js/clmtrackr.js"></script>
// <script src="./js/Filesaver.min.js"></script>
// <script src="./models/model_pca_20_svm.js"></script>

function getAllPositions(length) {
  var all_positions = [];

  for (i = 0; i < length; i++) {
    all_positions[i] = drawFeature(i);
  }
  return all_positions;
}

function drawFeatures(i) {
  var imageCC = document.getElementById('image' + i).getContext('2d');
  var canvasInput = document.getElementById('canvas' + i);
  var cc = canvasInput.getContext('2d');

  var ctracker = new clm.tracker({stopOnConvergence : true});
  ctracker.init(pModel);
  ctracker.start(document.getElementById('image' + i));

  var drawRequest;
  function drawLoop() {
    drawRequest = requestAnimationFrame(drawLoop);
    cc.clearRect(0, 0, canvasInput.width, canvasInput.height);
    ctracker.draw(canvasInput);
  }
  drawLoop();

  document.addEventListener("clmtrackrConverged", function(event) {
    document.getElementById('convergence').innerHTML = "CONVERGED";
    cancelRequestAnimFrame(drawRequest);
    return converged_pos = ctracker.getCurrentPosition();
  }, false);
}

