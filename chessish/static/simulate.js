var board = Chessboard('myBoard')

function simulate(pgn1) {
console.log(pgn1);
const chess1 = new Chess();
const chess2 = new Chess();
const startPos = chess2.fen();
const pgn = pgn1 /*[
  '[Event "Casual Game"]',
  '[Site "Berlin GER"]',
  '[Date "1852.??.??"]',
  '[EventDate "?"]',
  '[Round "?"]',
  '[Result "1-0"]',
  '[White "Adolf Anderssen"]',
  '[Black "Jean Dufresne"]',
  '[ECO "C52"]',
  '[WhiteElo "?"]',
  '[BlackElo "?"]',
  '[PlyCount "47"]',
  '',
  '1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Ba5 6.d4 exd4 7.O-O',
  'd3 8.Qb3 Qf6 9.e5 Qg6 10.Re1 Nge7 11.Ba3 b5 12.Qxb5 Rb8 13.Qa4',
  'Bb6 14.Nbd2 Bb7 15.Ne4 Qf5 16.Bxd3 Qh5 17.Nf6+ gxf6 18.exf6',
  'Rg8 19.Rad1 Qxf3 20.Rxe7+ Nxe7 21.Qxd7+ Kxd7 22.Bf5+ Ke8',
  '23.Bd7+ Kf8 24.Bxe7# 1-0',
] */

console.log(chess1.load_pgn(pgn/*.join('\n')*/));
let fens = chess1.history().map(move => {
  chess2.move(move);
  return chess2.fen();
});

//the above technique will not capture the fen of the starting position.  therefore:
fens = [startPos, ...fens];

var arrayLength = fens.length;
for (let i = 0; i < arrayLength; i++) {
  var tmp = fens[i];
  console.log(tmp);
  simulatePositions(tmp, i);
}
}

function simulatePositions(tmp, i) {
 setTimeout(function() {
     board.position(tmp);
 }, 2000 * i);
}

engine.onmessage = function(event) {
  var line = event.data;
  if(line == 'uciok') {
      engineStatus.engineLoaded = true;
  } else if(line == 'readyok') {
      engineStatus.engineReady = true;
  } else {
      var match = line.match(/^bestmove ([a-h][1-8])([a-h][1-8])([qrbk])?/);
      if(match) {
          isEngineRunning = false;
          game.move({from: match[1], to: match[2], promotion: match[3]});
          prepareMove();
      } else if(match = line.match(/^info .*\bdepth (\d+) .*\bnps (\d+)/)) {
          engineStatus.search = 'Depth: ' + match[1] + ' Nps: ' + match[2];
      }
      if(match = line.match(/^info .*\bscore (\w+) (-?\d+)/)) {
          var score = parseInt(match[2]) * (game.turn() == 'w' ? 1 : -1);
          if(match[1] == 'cp') {
              engineStatus.score = (score / 100.0).toFixed(2);
          } else if(match[1] == 'mate') {
              engineStatus.score = '#' + score;
          }
          if(match = line.match(/\b(upper|lower)bound\b/)) {
              engineStatus.score = ((match[1] == 'upper') == (game.turn() == 'w') ? '<= ' : '>= ') + engineStatus.score
          }
      }
  }
  displayStatus();
};

//console.log(pgn1);


//}
//Code 2

/*var a = chess.history();
a.forEach(function(entry) {
  board.move(entry);
});*/


/* const chess = new Chess()
const pgn = [
  '[Event "Casual Game"]',
  '[Site "Berlin GER"]',
  '[Date "1852.??.??"]',
  '[EventDate "?"]',
  '[Round "?"]',
  '[Result "1-0"]',
  '[White "Adolf Anderssen"]',
  '[Black "Jean Dufresne"]',
  '[ECO "C52"]',
  '[WhiteElo "?"]',
  '[BlackElo "?"]',
  '[PlyCount "47"]',
  '',
  '1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Ba5 6.d4 exd4 7.O-O',
  'd3 8.Qb3 Qf6 9.e5 Qg6 10.Re1 Nge7 11.Ba3 b5 12.Qxb5 Rb8 13.Qa4',
  'Bb6 14.Nbd2 Bb7 15.Ne4 Qf5 16.Bxd3 Qh5 17.Nf6+ gxf6 18.exf6',
  'Rg8 19.Rad1 Qxf3 20.Rxe7+ Nxe7 21.Qxd7+ Kxd7 22.Bf5+ Ke8',
  '23.Bd7+ Kf8 24.Bxe7# 1-0',
]

chess.load_pgn(pgn.join('\n'))
*/
// Code 2
/* for (let i=0; i<10; i++) {
  simulatePositions(i);
} */
//const pgn = `1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Ba5 6.d4 exd4 7.O-O`; 
