var board = null
var game = new Chess()
function onDragStart (source, piece, position, orientation) {
    console.log('Drag started:')
    console.log('Source: ' + source)
    console.log('Piece: ' + piece)
    console.log('Position: ' + Chessboard.objToFen(position))
    console.log('Orientation: ' + orientation)
    console.log('~~~~~~')
  }


function onDrop (source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null) return 'snapback'

  // make random legal move for black
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
  board.position()
}

var config = {
  draggable: true,
  position: frcGen(math.round(math.random() * 1000)),
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
}
board = Chessboard('myBoard', config)
// Some illegal moves are allowed: this is fine, as there is no public repo for 960 ruleset. 