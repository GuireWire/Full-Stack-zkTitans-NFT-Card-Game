// backgrounds
import heroImg from './background/hero-img.jpg';
import jungle from './background/jungle-battleground.jpg';
import volcano from './background/volcano-battleground.jpg';
import wasteland from './background/wasteland-battleground.jpg';
import swamp from './background/swamp-battleground.jpg';
import underwater from './background/underwater-battleground.jpg';
import space from './background/space-battleground.jpg';

// cards
import akuaku from './Aku_Aku-Hero.png';
import arachnina from './Arachnina-Titan.png';
import coco from './Coco-Hero.png';
import crash from './Crash-Hero.png';
import crunch from './Crunch-Hero.png';
import doommonkey from './Doom-Monkey-Minion.png';
import eelectric from './Ee-lectric-Titan.png';
import magmadon from './Magmadon-Titan.png';
import ngin from './N-Gin-Villain.png';
import neocortex from './Neo_Cortex-Villain.png';
import ninacortex from './Nina_Cortex-Villain.png';
import ratclicledoll from './Ratclicle_Doll-Battle-Doll.png';
import ratnician from './Ratnician-Minion.png';
import rhinoroller from './Rhinoroller-Titan.png';
import scorporilla from './Scorporilla-Titan.png';
import shellephant from './Shellephant-Titan.png';
import snipedoll from './Snipe_Doll-Battle-Doll.png';
import thebattler from './The_Battler-Titan.png';
import thebratgirl from './The_Bratgirl-Minion.png';
import thegoar from './The_Goar-Titan.png';
import thekooala from './The_Koo-Ala-Minion.png';
import theraticlicle from './The_Ratclicle-Titan.png';
import thesludge from './The_Sludge-Titan.png';
import thesnipe from './The_Snipe-Titan.png';
import thespike from './The_Spike-Titan.png';
import thestench from './The_Stench-Titan.png';
import ukaukatitan from './Uka_Uka-Titan.png';
import ulaukavillain from './Uka_Uka-Villain.png';
import voodoobunny from './Voodoo_Bunny-Minion.png';
import yuktopus from './Yuktopus-Titan.png';

// logo
import logo from './logo.png';

// icon
import attack from './attack.png';
import defense from './defense.png';
import alertIcon from './alertIcon.svg';
import AlertIcon from './AlertIcon.jsx';

// players
import player01 from './player01.png';
import player02 from './player02.png';

// sounds
import attackSound from './sounds/attack.mp3';
import defenseSound from './sounds/defense.mp3';
import explosion from './sounds/explosion.mp3';

export const allCards = [
  akuaku,
  arachnina,
  coco,
  crash,
  crunch,
  doommonkey,
  eelectric,
  magmadon,
  ngin,
  neocortex,
  ninacortex,
  ratclicledoll,
  ratnician,
  rhinoroller,
  scorporilla,
  shellephant,
  snipedoll,
  thebattler,
  thebratgirl,
  thegoar,
  thekooala,
  theraticlicle,
  thesludge,
  thesnipe,
  thespike,
  thestench,
  ukaukatitan,
  ulaukavillain,
  voodoobunny,
  yuktopus,
];

export {
  jungle,
  volcano,
  wasteland,
  swamp,
  underwater,
  space,
  heroImg,

  akuaku,
  arachnina,
  coco,
  crash,
  crunch,
  doommonkey,
  eelectric,
  magmadon,
  ngin,
  neocortex,
  ninacortex,
  ratclicledoll,
  ratnician,
  rhinoroller,
  scorporilla,
  shellephant,
  snipedoll,
  thebattler,
  thebratgirl,
  thegoar,
  thekooala,
  theraticlicle,
  thesludge,
  thesnipe,
  thespike,
  thestench,
  ukaukatitan,
  ulaukavillain,
  voodoobunny,
  yuktopus,

  logo,

  attack,
  defense,
  alertIcon,
  AlertIcon,

  player01,
  player02,

  attackSound,
  defenseSound,
  explosion,
};

export const battlegrounds = [
  { id: 'bg-jungle', image: jungle, name: 'Jungle' },
  { id: 'bg-volcano', image: volcano, name: 'Volcano' },
  { id: 'bg-wasteland', image: wasteland, name: 'Wasteland' },
  { id: 'bg-swamp', image: swamp, name: 'Swamp' },
  { id: 'bg-underwater', image: underwater, name: 'Underwater' },
  { id: 'bg-space', image: space, name: 'Space' },
];

export const gameRules = [
  'Card with the same defense and attack point will cancel each other out.',
  'Attack points from the attacking card will deduct the opposing player’s health points.',
  'If P1 does not defend, their health wil be deducted by P2’s attack.',
  'If P1 defends, P2’s attack is equal to P2’s attack - P1’s defense.',
  'If a player defends, they refill 3 Mana',
  'If a player attacks, they spend 3 Mana',
];