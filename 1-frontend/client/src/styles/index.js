const styles = {
  // general
  headText: 'font-crash font-normal text-white sm:text-8xl text-6xl',
  normalText: 'font-crash font-normal text-4xl text-siteWhite',
  footerText: 'font-crash font-normal text-3xl text-white',
  infoText: 'font-crash font-normal text-3xl text-siteOrange cursor-pointer',

  // glassmorphism
  glassEffect: 'bg-white backdrop-filter backdrop-blur-lg bg-opacity-10',

  // hoc page
  hocContainer: 'min-h-screen flex xl:flex-row flex-col relative',
  hocContentBox: 'flex flex-1 justify-between bg-siteblack py-8 sm:px-12 px-8 flex-col',
  hocLogo: 'w-[320px] h-[104px] object-contain cursor-pointer',
  hocBodyWrapper: 'flex-1 flex justify-center flex-col xl:mt-0 my-16',

  // join battle page
  joinHeadText: 'font-crash font-normal text-6xl text-white mb-6',
  joinContainer: 'flex flex-col gap-6 mt-3 mb-8',
  joinBattleTitle: 'font-crash font-normal text-4xl text-white',
  joinLoading: 'font-crash font-normal text-3xl text-white',

  // battleground page
  battlegroundContainer: 'min-h-screen bg-landing flex-col py-12 px-4',
  battleGroundsWrapper: 'flex-wrap mt-10 max-w-[1200px]',
  battleGroundCard: 'sm:w-[480px] w-full h-[297px] p-2 glass-morphism m-4 rounded-lg cursor-pointer battle-card',
  battleGroundCardImg: 'w-full h-full object-cover rounded-md',
  battleGroundCardText: 'font-crash font-normal text-6xl text-white',

  // Game page
  gameContainer: 'w-screen min-h-screen bg-cover bg-no-repeat bg-center flex-col',
  gameMoveBox: 'sm:w-20 w-14 sm:h-20 h-14 rounded-full cursor-pointer border-[2px]',
  gameMoveIcon: 'w-1/2 h-1/w-1/2 object-contain',

  // player info component
  playerImg: 'w-14 h-14 object-contain rounded-full',
  playerHealth: 'flex flex-row bg-white rounded-md p-2 sm:min-w-[512px] min-w-[312px] sm:min-h-[48px] min-h-[40px] bg-opacity-10 backdrop-filter backdrop-blur-lg mx-3',
  playerHealthBar: 'sm:w-4 w-2 sm:h-8 h-6 rounded-sm',
  playerMana: 'w-14 h-14 rounded-full text-white font-crash font-normal text-4xl cursor-pointer',
  playerInfo: 'font-chau font-normal text-l',
  playerInfoSpan: 'font-extrabold text-white',

  // card component
  cardContainer: 'relative sm:w-[260px] w-[220px] sm:h-[335px] h-[280px] z-0 transition-all',
  cardImg: 'w-full h-full object-contain ml-2',
  cardPointContainer: 'absolute sm:w-[40px] w-[32px] sm:h-[40px] h-[32px] rounded-[25px] bottom-[12%]',
  cardPoint: 'font-crash text-5xl font-normal',
  cardTextContainer: 'absolute w-full bottom-[-8.5%] left-26',
  cardText: 'font-crash text-5xl font-normal text-white',

  // custom button component
  btn: 'px-8 py-3 rounded-lg bg-siteOrange w-fit text-white font-crash font-normal text-4xl',

  // custom input component
  label: 'font-crash font-normal text-6xl text-white mb-6',
  input: 'bg-siteDimBlack text-white font-chau font-bold text-xl outline-none focus:outline-siteOrange p-6 rounded-md sm:max-w-[50%] max-w-full',

  // gameload component
  gameLoadContainer: 'absolute inset-0 z-10 w-full h-screen gameload flex-col',
  gameLoadBtnBox: 'w-full flex justify-end px-8',
  gameLoadText: 'font-crash text-siteWhite text-4xl mt-5 text-center',
  gameLoadPlayersBox: 'flex justify-evenly items-center mt-20',
  gameLoadPlayerImg: 'md:w-52 w-40 md:h-52 h-40 object-contain rounded-full drop-shadow-lg',
  gameLoadPlayerText: 'mt-3 font-crash text-white md:text-3xl text-2xl w-[250px] text-center truncate',
  gameLoadVS: 'font-crash font-normal text-siteOrange text-9xl mx-16',

  // gameInfo component
  gameInfoIconBox: 'absolute right-2 top-1/2',
  gameInfoIcon: 'bg-siteOrange w-14 h-14 rounded-md cursor-pointer',
  gameInfoIconImg: 'w-10 h-10 object-contain invert',
  gameInfoSidebar: 'absolute p-6 right-0 top-0 h-screen rounded-md flex-col transition-all ease-in duration-300',
  gameInfoSidebarCloseBox: 'flex justify-end mb-8',
  gameInfoSidebarClose: 'w-10 h-10 rounded-md bg-siteOrange text-white font-crash font-normal text-4xl cursor-pointer',
  gameInfoHeading: 'font-crash font-normal text-white text-6xl',
  gameInfoText: 'font-crash font-normal text-white text-4xl mb-2',

  // common
  flexCenter: 'flex items-center justify-center',
  flexEnd: 'flex justify-end items-end',
  flexBetween: 'flex justify-between items-center',

// alert
info: 'text-blue-700 bg-blue-100 dark:bg-blue-200 dark:text-blue-800',
success: 'text-green-700 bg-green-100 dark:bg-green-200 dark:text-green-800',
failure: 'text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800',
alertContainer: 'absolute z-10 top-10 left-0 right-0',
alertWrapper: 'p-4 rounded-lg font-crash font-normal text-3xl', // Reduced padding and text size
alertIcon: 'flex-shrink-0 inline w-8 h-8 mr-3', // Reduced icon size and margin

  // modal
  modalText: 'font-crash font-normal text-5xl text-white mb-6 text-center',
};

export default styles;
