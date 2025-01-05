# pragma version 0.4.0

"""
@license MIT
@title zkTitans
@author GuireWire
@notice This contract handles the token management and battle logic for the zkTitans game. This is a personal, non-commercial fan project heavily inspired by Activision's Crash Bandicoot Crash of the Titans
@dev This project is not affiliated with, endorsed by, or connected to Activision Publishing, Inc.
"""

# ------------------------------------------------------------------
#                  INTERFACES - FLATTENED VERSION
# ------------------------------------------------------------------

interface IERC1155:
    def supportsInterface(interfaceId: bytes4) -> bool: view
    def safeTransferFrom(_from: address, _to: address, _id: uint256, _value: uint256, _data: Bytes[1_024]): nonpayable  
    def safeBatchTransferFrom(_from: address, _to: address, _ids: DynArray[uint256, 128], _values: DynArray[uint256, 128], _data: Bytes[1_024]): nonpayable
    def balanceOf(_owner: address, _id: uint256) -> uint256: view
    def balanceOfBatch(_owners: DynArray[address, 128], _ids: DynArray[uint256, 128]) -> DynArray[uint256, 128]: view 
    def setApprovalForAll(_operator: address, _approved: bool): nonpayable
    def isApprovedForAll(_owner: address, _operator: address) -> bool: view

interface IERC1155Receiver:
    def onERC1155Received(_operator: address, _from: address, _id: uint256, _value: uint256, _data: Bytes[1_024]) -> bytes4: nonpayable
    def onERC1155BatchReceived(_operator: address, _from: address, _ids: DynArray[uint256, 128], _values: DynArray[uint256, 128], _data: Bytes[1_024]) -> bytes4: nonpayable

interface IERC1155MetadataURI:
    def uri(_id: uint256) -> String[512]: view

# ERC1155 Events
event TransferSingle:
    _operator: indexed(address)
    _from: indexed(address)
    _to: indexed(address)
    _id: uint256
    _value: uint256

event TransferBatch:
    _operator: indexed(address)
    _from: indexed(address)
    _to: indexed(address)
    _ids: DynArray[uint256, 128]
    _values: DynArray[uint256, 128]

event ApprovalForAll:
    _owner: indexed(address)
    _operator: indexed(address)
    _approved: bool

# ------------------------------------------------------------------
#                   IMPORTS - FLATTENED VERSION
# ------------------------------------------------------------------

# ERC165 and ERC1155 Interface IDs
IERC165_ID: constant(bytes4) = 0x01FFC9A7
IERC1155_ID: constant(bytes4) = 0xD9B67A26 
IERC1155_METADATA_ID: constant(bytes4) = 0x0E89341C

event URI:
    _value: String[512]
    _id: indexed(uint256)

# Ownable Implementation
owner: public(address)

event OwnershipTransferred:
    previous_owner: indexed(address)
    new_owner: indexed(address)

@internal
def _check_owner():
    """
    @dev Throws if the sender is not the owner.
    """
    assert msg.sender == self.owner, "ownable: caller is not the owner"

@internal
def _transfer_ownership(new_owner: address):
    """
    @dev Transfers the ownership of the contract to a new account `new_owner`.
    @notice This is an internal function without access restriction.
    @param new_owner The 20-byte address of the new owner.
    """
    old_owner: address = self.owner
    self.owner = new_owner
    log OwnershipTransferred(old_owner, new_owner)

@external
def transfer_ownership(new_owner: address):
    """
    @dev Transfers the ownership of the contract to a new account `new_owner`.
    @notice Note that this function can only be called by the current `owner`.
    @param new_owner The 20-byte address of the new owner.
    """
    self._check_owner()
    assert new_owner != empty(address), "ownable: new owner is the zero address"
    self._transfer_ownership(new_owner)

@external
def renounce_ownership():
    """
    @dev Leaves the contract without owner. Only callable by current owner.
    @notice Renouncing ownership will leave the contract without an owner,
            removing any functionality that is only available to the owner.
    """
    self._check_owner()
    self._transfer_ownership(empty(address))

# ERC1155 Implementation
@internal
def _mint(to: address, id: uint256, amount: uint256, data: Bytes[1024]):
    """
    @dev Internal function to mint tokens
    @param to The address that will receive the minted token
    @param id The token id to mint
    @param amount The amount of tokens to mint
    @param data Additional data to pass along
    """
    assert to != empty(address), "ERC1155: mint to the zero address"
    
    # Update balances
    self._balances[id][to] += amount
    self.TOTAL_SUPPLY += amount
    
    # Emit transfer event
    log URI(concat(self.BASE_URI, ""), id)
    log TransferSingle(msg.sender, empty(address), to, id, amount)
    
    # If `to` is a contract, verify ERC1155Receiver implementation
    if to.is_contract:
        response: bytes4 = extcall IERC1155Receiver(to).onERC1155Received(msg.sender, empty(address), id, amount, data)
        assert response == method_id("onERC1155Received(address,address,uint256,uint256,bytes)", output_type=bytes4)

# ------------------------------------------------------------------
#                         STATE VARIABLES
# ------------------------------------------------------------------

BASE_URI: public(String[512])
TOTAL_SUPPLY: public(uint256)
_balances: HashMap[uint256, HashMap[address, uint256]]
_operatorApprovals: HashMap[address, HashMap[address, bool]]
MAX_ATTACK_DEFEND_STRENGTH: public(constant(uint256)) = 10

# Card Type Constants
AKUAKU: public(constant(uint256)) = 0
ARACHNINA: public(constant(uint256)) = 1
COCO: public(constant(uint256)) = 2
CRASH: public(constant(uint256)) = 3
CRUNCH: public(constant(uint256)) = 4
DOOMMONKEY: public(constant(uint256)) = 5
EELECTRIC: public(constant(uint256)) = 6
MAGMADON: public(constant(uint256)) = 7
NGIN: public(constant(uint256)) = 8
NEOCORTEX: public(constant(uint256)) = 9
NINACORTEX: public(constant(uint256)) = 10
RATCICLEDOLL: public(constant(uint256)) = 11
RATNICIAN: public(constant(uint256)) = 12
RHINOROLLER: public(constant(uint256)) = 13
SCORPORILLA: public(constant(uint256)) = 14
SHELLEPHANT: public(constant(uint256)) = 15
SNIPEDOLL: public(constant(uint256)) = 16
THEBATTLER: public(constant(uint256)) = 17
THEBRATGIRL: public(constant(uint256)) = 18
THEGOAR: public(constant(uint256)) = 19
THEKOOALA: public(constant(uint256)) = 20
THERATICLICLE: public(constant(uint256)) = 21
THESLUDGE: public(constant(uint256)) = 22
THESNIPE: public(constant(uint256)) = 23
THESPIKE: public(constant(uint256)) = 24
THESTENCH: public(constant(uint256)) = 25
UKAUKATITAN: public(constant(uint256)) = 26
ULAUKAVILLAIN: public(constant(uint256)) = 27
VOODOOBUNNY: public(constant(uint256)) = 28
YUKTOPUS: public(constant(uint256)) = 29

# Maximum number of card types
MAX_CARD_TYPES: public(constant(uint256)) = 30

# ------------------------------------------------------------------
#                              FLAGS
# ------------------------------------------------------------------

# @dev Battle status flag type
flag BattleStatus:
    PENDING 
    STARTED
    ENDED

# ------------------------------------------------------------------
#                             STRUCTS
# ------------------------------------------------------------------


# @dev GameToken struct to store player token info
# @param name - Battle Card Name, set by player
# @param id - Battle Card Token ID, this is randomly generated
# @param attackStrength - Battle Card Attack, generated randomly
# @param defenseStrength - Battle Card Attack, generated randomly
struct GameToken:
    name: String[1000]
    id: uint256
    attackStrength: uint256
    defenseStrength: uint256

# @dev Player struct to store player info
# @param playerAddress - Player Wallet Address
# @param playerName - Player Name, set by player during registration
# @param playerMana - Player Mana, affected by battle results
# @param playerHealth - Player Health, affected by battle results
# @param inBattle - Bool that Indicates if player is in battle
struct Player:
    playerAddress: address
    playerName: String[100]
    playerMana: uint256
    playerHealth: uint256
    inBattle: bool

# @dev Battle struct to store battle info
# @param battleStatus - flag to indicate battle status
# @param battleHash - hash of the battle name
# @param name - Battle Name, set by player who created the battle
# @param players - players address array representing the players in the battle (max 2)
# @param moves - array representing players' moves
# @param winner - winner address
struct Battle:
    battleStatus: BattleStatus
    battleHash: bytes32
    name: String[100]
    players: address[2]
    moves: uint8[2]
    winner: address

# @dev Player battle stats struct
# @param index Player's index in the players array
# @param move Player's current move (1 for attack, 2 for defense)
# @param health Player's current health points
# @param attack Player's attack strength from their game token
# @param defense Player's defense strength from their game token
struct P:
    index: uint256
    move: uint256
    health: uint256
    attack: uint256
    defense: uint256

# ------------------------------------------------------------------
#                             MAPPINGS
# ------------------------------------------------------------------

# @dev Mapping of player addresses to player index in the players array
playerInfo: public(HashMap[address, uint256])

# @dev Mapping of player addresses to player token index in the gameTokens array
playerTokenInfo: public(HashMap[address, uint256])

# @dev Mapping of battle name to battle index in the battles array
battleInfo: public(HashMap[String[1000], uint256])

# ------------------------------------------------------------------
#                              ARRAYS
# ------------------------------------------------------------------

# @dev Array of players addresses
players: public(DynArray[Player, 5000])
gameTokens: public(DynArray[GameToken, 10000])
battles: public(DynArray[Battle, 20000])

# ------------------------------------------------------------------
#                              EVENTS
# ------------------------------------------------------------------

event NewPlayer:
    owner: indexed(address)
    name: String[100]

event NewBattle:
    battleName: String[100]
    player1: indexed(address)
    player2: indexed(address)

event BattleEnded:
    battleName: String[100]
    winner: indexed(address)
    loser: indexed(address)

event BattleMove:
    battleName: indexed(String[100])
    isFirstMove: indexed(bool)

event NewGameToken:
    owner: indexed(address)
    id: uint256
    attackStrength: uint256
    defenseStrength: uint256

event RoundEnded:
    damagedPlayers: address[2]

event Debug:
    message: String[100]

# ------------------------------------------------------------------
#                           CONSTRUCTOR
# ------------------------------------------------------------------

@deploy
def __init__(_base_uri: String[512]):
    """
    @dev Initialize contract with base URI for token metadata
    """
    self.BASE_URI = _base_uri
    
    # Initialize with dummy first entries
    self.players.append(Player(
        playerAddress=empty(address),
        playerName="",
        playerMana=0,
        playerHealth=0,
        inBattle=False
    ))
    
    self.gameTokens.append(GameToken(
        name="",
        id=0,
        attackStrength=0,
        defenseStrength=0
    ))
    
    # Initialize owner
    self._transfer_ownership(msg.sender)
    log URI(concat(_base_uri, ""), 0)

# ------------------------------------------------------------------
#                     INTERNAL VIEW FUNCTIONS
# ------------------------------------------------------------------

@view
@internal
def _createRandomNum(_max: uint256, _sender: address) -> uint256:
    """
    @dev Internal function to generate random number; used for Battle Card Attack and Defense Strength
    @param _max Maximum value for the random number
    @param _sender Address to use in random number generation
    @return Random value between 1 and _max
    """
    randomNum: uint256 = convert(
        keccak256(
            concat(
                block.prevrandao,
                convert(block.timestamp, bytes32),
                convert(_sender, bytes32)
            )
        ),
        uint256
    )
    
    randomValue: uint256 = randomNum % _max
    if randomValue == 0:
        randomValue = _max // 2
        
    return randomValue

# ------------------------------------------------------------------
#                        INTERNAL FUNCTIONS
# ------------------------------------------------------------------

@internal
def initialize():
    """
    @dev Initializes the contract with empty default values for gameTokens, players, and battles arrays
    """
    # Initialize gameTokens with empty token
    self.gameTokens.append(GameToken(
        name="",
        id=0,
        attackStrength=0,
        defenseStrength=0
    ))
    # Initialize players with empty player
    self.players.append(Player(
        playerAddress=empty(address),
        playerName="",
        playerMana=0,
        playerHealth=0,
        inBattle=False
    ))
    # Initialize battles with empty battle
    self.battles.append(Battle(
        battleStatus=BattleStatus.PENDING,
        battleHash=empty(bytes32),
        name="",
        players=[empty(address), empty(address)],
        moves=[0, 0],
        winner=empty(address)
    ))

@internal
def updateBattle(_name: String[100], _newBattle: Battle):
    """
    @dev Updates an existing battle with new battle data.
    @param _name - The name of the battle to update.
    @param _newBattle - The new battle data to store.
    """
    _battle_index: uint256 = self.battleInfo[_name]
    assert _battle_index != 0, "Battle doesn't exist"
    # Use 1-based indexing by subtracting 1 from battle index
    self.battles[_battle_index - 1] = _newBattle

@internal
def _createGameToken(_name: String[1000]) -> GameToken:
    """
    @dev Internal function to create a new Battle Card
    @param _name Name of the battle card
    @return New game token
    """
    # Generate random attack and defense strengths
    randAttackStrength: uint256 = self._createRandomNum(MAX_ATTACK_DEFEND_STRENGTH, msg.sender)
    randDefenseStrength: uint256 = MAX_ATTACK_DEFEND_STRENGTH - randAttackStrength

    # Generate random ID between 1 and 5
    randId: uint8 = convert(
        convert(
            keccak256(
                concat(
                    convert(block.timestamp, bytes32),
                    convert(msg.sender, bytes32)
                )
            ),
            uint256
        ) % 100,
        uint8
    )
    randId = randId % 30
    if randId == 0:
        randId = 1

    # Create new game token
    newGameToken: GameToken = GameToken(
        name=_name,
        id=convert(randId, uint256),
        attackStrength=randAttackStrength,
        defenseStrength=randDefenseStrength
    ) 

    # Add token to storage
    _id: uint256 = len(self.gameTokens)
    self.gameTokens.append(newGameToken)
    self.playerTokenInfo[msg.sender] = _id

    # Mint the token
    self._mint(msg.sender, convert(randId, uint256), 1, b"")

    # Emit new token event
    log NewGameToken(msg.sender, convert(randId, uint256), randAttackStrength, randDefenseStrength)

    return newGameToken

@internal
def _registerPlayerMove(_player: uint256, _choice: uint8, _battleName: String[100]):
    """
    @dev Internal function to register a player's move in a battle
    @param _player Index of the player (0 or 1)
    @param _choice Move choice (1 for attack, 2 for defense)
    @param _battleName Name of the battle
    """
    # Verify valid move choice
    assert _choice == 1 or _choice == 2, "Choice should be either 1 or 2!"

    # Check mana if attacking
    if _choice == 1:
        player: Player = self.players[self.playerInfo[msg.sender]]
        assert player.playerMana >= 3, "Mana not sufficient for attacking!"

    # Update move in battle
    _battle_index: uint256 = self.battleInfo[_battleName]
    assert _battle_index != 0, "Battle doesn't exist!"
    self.battles[_battle_index - 1].moves[_player] = _choice  # Using 1-based indexing

@internal
def _awaitBattleResults(_battleName: String[100]):
    """
    @dev Internal function to check if battle can be resolved and trigger resolution
    @param _battleName Name of the battle
    """
    # Get battle from storage
    _battle_index: uint256 = self.battleInfo[_battleName]
    assert _battle_index != 0, "Battle doesn't exist!"
    
    # Use 1-based indexing for battles array
    _battle: Battle = self.battles[_battle_index - 1]
    
    # Check if sender is a player in the battle
    assert msg.sender == _battle.players[0] or msg.sender == _battle.players[1], "Only players in this battle can make a move"
    
    # Check if both players have made their moves
    assert _battle.moves[0] != 0 and _battle.moves[1] != 0, "Players still need to make a move"
    
    # Resolve the battle
    self._resolveBattle(_battle)
    
    # Update the battle in storage with 1-based indexing
    self.battles[_battle_index - 1] = _battle

@internal
def _resolveBattle(_battle: Battle):
    """
    @dev Resolve battle function to determine winner and loser of battle
    @param _battle Battle struct containing the current battle state
    """
    # Initialize player 1 battle stats
    p1: P = P(
        index=self.playerInfo[_battle.players[0]],
        move=convert(_battle.moves[0], uint256),
        health=self.players[self.playerInfo[_battle.players[0]]].playerHealth,
        attack=self.gameTokens[self.playerTokenInfo[_battle.players[0]]].attackStrength,
        defense=self.gameTokens[self.playerTokenInfo[_battle.players[0]]].defenseStrength
    )

    # Initialize player 2 battle stats
    p2: P = P(
        index=self.playerInfo[_battle.players[1]],
        move=convert(_battle.moves[1], uint256),
        health=self.players[self.playerInfo[_battle.players[1]]].playerHealth,
        attack=self.gameTokens[self.playerTokenInfo[_battle.players[1]]].attackStrength,
        defense=self.gameTokens[self.playerTokenInfo[_battle.players[1]]].defenseStrength
    )

    # Initialize common variables
    _damaged_players: address[2] = [_battle.players[0], _battle.players[1]]
    healthAfterAttack: uint256 = 0
    PHAD: uint256 = 0
    damage: uint256 = 0

    # Both players attack
    if p1.move == 1 and p2.move == 1:
        log Debug("Both players attacked")
        
        # Calculate new health values with safe math
        new_p1_health: uint256 = p1.health
        new_p2_health: uint256 = p2.health

        if p2.attack >= new_p1_health:
            new_p1_health = 0
        else:
            new_p1_health = p1.health - p2.attack

        if p1.attack >= new_p2_health:
            new_p2_health = 0
        else:
            new_p2_health = p2.health - p1.attack

        # Update health
        self.players[p1.index].playerHealth = new_p1_health
        self.players[p2.index].playerHealth = new_p2_health

        # Update mana (ensure it doesn't go below 0)
        p1_mana: uint256 = self.players[p1.index].playerMana
        p2_mana: uint256 = self.players[p2.index].playerMana
        self.players[p1.index].playerMana = p1_mana - min(p1_mana, 3)
        self.players[p2.index].playerMana = p2_mana - min(p2_mana, 3)
        
        # Reset moves before checking for defeat
        _battle.moves = [convert(0, uint8), convert(0, uint8)]
        self.updateBattle(_battle.name, _battle)
        
        # Emit round ended event
        log RoundEnded(_damaged_players)

        # Check for defeat after damage - handle simultaneous death
        if new_p1_health == 0 and new_p2_health == 0:
            if p1.attack > p2.attack:
                _battle = self._endBattle(_battle.players[0], _battle)
            else:
                _battle = self._endBattle(_battle.players[1], _battle)
        elif new_p1_health == 0:
            _battle = self._endBattle(_battle.players[1], _battle)
        elif new_p2_health == 0:
            _battle = self._endBattle(_battle.players[0], _battle)
        else:
            # Update random stats if battle continues
            self._updateRandomStats(_battle)
        return

    # Player 1 attacks, Player 2 defends
    elif p1.move == 1 and p2.move == 2:
        log Debug("P1 attacks, P2 defends")
        PHAD = p2.health + p2.defense
        damage = p1.attack
        
        if p2.defense >= damage:
            healthAfterAttack = p2.health
        else:
            healthAfterAttack = PHAD - min(damage, PHAD)

        # Update health and mana
        self.players[p2.index].playerHealth = healthAfterAttack

        # Update mana
        p1_mana: uint256 = self.players[p1.index].playerMana
        p2_mana: uint256 = self.players[p2.index].playerMana
        self.players[p1.index].playerMana = p1_mana - min(p1_mana, 3)
        self.players[p2.index].playerMana = min(p2_mana + 3, 25)
        
        # Reset moves before checking for defeat
        _battle.moves = [convert(0, uint8), convert(0, uint8)]
        self.updateBattle(_battle.name, _battle)
        
        # Emit round ended event
        _damaged_players[0] = _battle.players[1]
        log RoundEnded(_damaged_players)

        if healthAfterAttack == 0:
            _battle = self._endBattle(_battle.players[0], _battle)
        else:
            # Update random stats if battle continues
            self._updateRandomStats(_battle)
        return

    # Player 1 defends, Player 2 attacks
    elif p1.move == 2 and p2.move == 1:
        log Debug("P1 defends, P2 attacks")
        PHAD = p1.health + p1.defense
        damage = p2.attack
        
        if p1.defense >= damage:
            healthAfterAttack = p1.health
        else:
            healthAfterAttack = PHAD - min(damage, PHAD)

        # Update health and mana
        self.players[p1.index].playerHealth = healthAfterAttack

        # Update mana
        p1_mana: uint256 = self.players[p1.index].playerMana
        p2_mana: uint256 = self.players[p2.index].playerMana
        self.players[p1.index].playerMana = min(p1_mana + 3, 25)
        self.players[p2.index].playerMana = p2_mana - min(p2_mana, 3)
        
        # Reset moves before checking for defeat
        _battle.moves = [convert(0, uint8), convert(0, uint8)]
        self.updateBattle(_battle.name, _battle)
        
        # Emit round ended event
        _damaged_players[0] = _battle.players[0]
        log RoundEnded(_damaged_players)

        if healthAfterAttack == 0:
            _battle = self._endBattle(_battle.players[1], _battle)
        else:
            # Update random stats if battle continues
            self._updateRandomStats(_battle)
        return

    # Both players defend
    else:
        log Debug("Both players defended")
        
        # Update mana
        p1_mana: uint256 = self.players[p1.index].playerMana
        p2_mana: uint256 = self.players[p2.index].playerMana
        self.players[p1.index].playerMana = min(p1_mana + 3, 25)
        self.players[p2.index].playerMana = min(p2_mana + 3, 25)
        
        # Reset moves
        _battle.moves = [convert(0, uint8), convert(0, uint8)]
        self.updateBattle(_battle.name, _battle)
        
        # Emit round ended event
        log RoundEnded(_damaged_players)
        
        # Update random stats
        self._updateRandomStats(_battle)
        return

@internal
def _updateRandomStats(_battle: Battle):
    """
    @dev Helper function to update random attack and defense stats
    """
    _random_attack_p1: uint256 = self._createRandomNum(MAX_ATTACK_DEFEND_STRENGTH, _battle.players[0])
    self.gameTokens[self.playerTokenInfo[_battle.players[0]]].attackStrength = _random_attack_p1
    self.gameTokens[self.playerTokenInfo[_battle.players[0]]].defenseStrength = MAX_ATTACK_DEFEND_STRENGTH - _random_attack_p1

    _random_attack_p2: uint256 = self._createRandomNum(MAX_ATTACK_DEFEND_STRENGTH, _battle.players[1])
    self.gameTokens[self.playerTokenInfo[_battle.players[1]]].attackStrength = _random_attack_p2
    self.gameTokens[self.playerTokenInfo[_battle.players[1]]].defenseStrength = MAX_ATTACK_DEFEND_STRENGTH - _random_attack_p2

@internal
def _endBattle(battleEnder: address, _battle: Battle) -> Battle:
    """
    @dev Internal function to end the battle
    @param battleEnder Winner's address
    @param _battle Battle struct taken from attackOrDefend function
    @return Updated battle struct
    """
    # Get player indices
    p1: uint256 = self.playerInfo[_battle.players[0]]
    p2: uint256 = self.playerInfo[_battle.players[1]]

    # Reset both players' battle status
    self.players[p1].inBattle = False
    self.players[p2].inBattle = False

    # Set winner explicitly before changing status
    _battle.winner = battleEnder

    # Update status and reset moves
    _battle.battleStatus = BattleStatus.ENDED
    _battle.moves = [convert(0, uint8), convert(0, uint8)]

    # Determine loser (for event)
    _battleLoser: address = _battle.players[1] if battleEnder == _battle.players[0] else _battle.players[0]

    # Update battle in storage
    self.updateBattle(_battle.name, _battle)

    # Emit battle ended event
    log BattleEnded(_battle.name, battleEnder, _battleLoser)

    return _battle

# ------------------------------------------------------------------
#                     EXTERNAL VIEW FUNCTIONS
# ------------------------------------------------------------------

@view
@external
def isPlayer(addr: address) -> bool:
    """
    @dev Checks if a given address corresponds to a registered player.
    @param addr - The address to check.
    @return - True if the address is a registered player, False otherwise.
    """
    player_id: uint256 = self.playerInfo[addr]
    if player_id == 0:
        return False
    
    # Also verify the player exists in the array
    if player_id >= len(self.players):
        return False
        
    return self.players[player_id].playerAddress == addr

@view
@external
def getPlayer(addr: address) -> Player:
    """
    @dev Fetches the player details by address.
    @param addr - The address of the player.
    @return - Player's address
    """
    
    # Check if the player exists
    assert self.playerInfo[addr] !=0, "Player doesn't exist!"

    # Return player details
    return self.players[self.playerInfo[addr]]

@view
@external
def getAllPlayers() -> DynArray[Player, 5000]:
    """
    @dev Returns array of all players.
    @return - Array of all registered players.
    """
    return self.players


@view
@external
def isPlayerToken(addr: address) -> bool:
    """
    @dev Checks if a given address has a game token.
    @param addr - The address to check.
    @return - True if the address has a token, False otherwise.
    """
    if self.playerTokenInfo[addr] == 0:
        return False
    else:
        return True    

@view
@external
def getPlayerToken(addr: address) -> GameToken:
    """
    @dev Fetches the game token details by player address.
    @param addr - The address of the player.
    @return - Player's game token.
    """
    # Check if the token exists
    assert self.playerTokenInfo[addr] != 0, "Game token doesn't exist!"

    # Return the game token
    return self.gameTokens[self.playerTokenInfo[addr]]

@view
@external
def getAllPlayerTokens() -> DynArray[GameToken, 10000]:
    """
    @dev Returns array of all game tokens.
    @return - Array of all game tokens.
    """
    return self.gameTokens

@view
@external
def getTotalSupply() -> uint256:
    """
    @dev Returns the total supply of all tokens
    @return Current total supply
    """
    return self.TOTAL_SUPPLY

@view 
@external 
def isBattle(_name: String[100]) -> bool:
    """
    @dev Checks if a battle with given name exists.
    @param _name - The name of the battle to check.
    @return - True if the battle exists, False otherwise.
    """
    battle_id: uint256 = self.battleInfo[_name]
    # Since we're using 1-based indexing, any non-zero ID means the battle exists
    return battle_id != 0

@view
@external
def getBattle(_name: String[100]) -> Battle:
    """
    @dev Gets battle information
    @param _name name of the battle
    @return Battle struct containing battle information
    """
    battle_id: uint256 = self.battleInfo[_name]
    assert battle_id != 0, "Battle doesn't exist!"
    # Since we're using 1-based indexing, need to subtract 1 for array access
    return self.battles[battle_id - 1]
    
@view
@external
def getAllBattles() -> DynArray[Battle, 20000]:
    """
    @dev Returns array of all battles.
    @return - Array of all battles in the game.
    """
    return self.battles

@view
@external
def getBattleMoves(_battleName: String[100]) -> (uint256, uint256):
    """
    @dev Read battle move info for player 1 and player 2
    @param _battleName The name of the battle
    @return (P1Move, P2Move) Tuple containing moves of both players
    """
    # Get battle from storage using battleInfo mapping
    _battle_index: uint256 = self.battleInfo[_battleName]
    assert _battle_index != 0, "Battle doesn't exist!"
    
    # Use 1-based indexing to get battle
    _battle: Battle = self.battles[_battle_index - 1]

    # Convert uint8 moves to uint256 and return
    return (
        convert(_battle.moves[0], uint256),
        convert(_battle.moves[1], uint256)
    )

# @view
# @external
# def tokenURI(tokenId: uint256) -> String[1000]:
#     """
#     @dev Returns the URI for a given token ID
#     @param tokenId The ID of the token to get the URI for
#     @return The token's URI
#     """
#     assert tokenId < MAX_CARD_TYPES, "Token ID out of range"
#     return concat(self.BASE_URI, convert(tokenId, String[100]), ".json")

# ------------------------------------------------------------------
#                        EXTERNAL FUNCTIONS
# ------------------------------------------------------------------

@external
def setURI(_new_uri: String[512]):
    """
    @dev Updates the base URI for token metadata
    @param _new_uri New base URI for all tokens
    """
    self._check_owner()
    self.BASE_URI = _new_uri
    log URI(concat(_new_uri, ""), 0)

@external
def registerPlayer(_name: String[100], _gameTokenName: String[1000]):
    """
    @dev Registers a player
    @param _name player name; set by player
    @param _gameTokenName name for the player's game token
    """
    # Require that player is not already registered
    assert self.playerInfo[msg.sender] == 0, "Player already registered"
    
    # Get new player ID (will be current length since we append)
    _id: uint256 = len(self.players)
    
    # Add player to players array
    self.players.append(Player(
        playerAddress=msg.sender,
        playerName=_name,
        playerMana=25,
        playerHealth=10,
        inBattle=False
    ))

    # Create Player info mapping
    self.playerInfo[msg.sender] = _id

    # Create Random Game Token
    self._createGameToken(_gameTokenName)

    # Emit NewPlayer Event
    log NewPlayer(msg.sender, _name)

@external
def createRandomGameToken(_name: String[1000]):
    """
    @dev Creates a new game token
    @param _name Game token name; set by player
    """
    # Check if player exists using direct mapping access
    assert self.playerInfo[msg.sender] != 0, "Please Register Player First"

    # Get player struct directly from storage
    player: Player = self.players[self.playerInfo[msg.sender]]
    assert not player.inBattle, "Player is in a battle"

    # Create the game token
    self._createGameToken(_name)

@external
def createBattle(_name: String[100]) -> Battle:
    """
    @dev Creates a new battle
    @param _name battle name; set by player
    @return Battle struct containing the new battle information
    """
    # Check if player is registered
    assert self.playerInfo[msg.sender] != 0, "Please Register Player First"

    # Check battle doesn't already exist
    assert self.battleInfo[_name] == 0, "Battle already exists!"

    # Create battle hash
    battleHash: bytes32 = keccak256(abi_encode(_name))  # Changed from _abi_encode to abi_encode

    # Create new battle struct
    _battle: Battle = Battle(
        battleStatus=BattleStatus.PENDING,
        battleHash=battleHash,
        name=_name,
        players=[msg.sender, empty(address)],
        moves=[convert(0, uint8), convert(0, uint8)],
        winner=empty(address)
    )

    # Set the battle ID first (using current length + 1)
    _id: uint256 = len(self.battles) + 1  # Changed from len - 1 to len + 1
    self.battleInfo[_name] = _id

    # Then add battle to storage
    self.battles.append(_battle)
    
    # Emit NewBattle event
    log NewBattle(_name, msg.sender, empty(address))
    
    return _battle

@external
def joinBattle(_name: String[100]) -> Battle:
    """
    @dev Player joins battle
    @param _name battle name; name of battle player wants to join
    @return Battle struct containing the updated battle information
    """
    # Get battle from storage
    _battle_index: uint256 = self.battleInfo[_name]
    assert _battle_index != 0, "No battle found"
    
    # Get battle data (using 1-based indexing)
    _battle: Battle = self.battles[_battle_index - 1]

    # Check player requirements
    assert self.playerInfo[msg.sender] != 0, "Player not registered"
    assert msg.sender != _battle.players[0], "Own battle"
    assert _battle.battleStatus == BattleStatus.PENDING, "Battle in progress"

    # Check if player is in battle
    player: Player = self.players[self.playerInfo[msg.sender]]
    assert not player.inBattle, "Already in battle"

    # Update battle
    _battle.battleStatus = BattleStatus.STARTED
    _battle.players[1] = msg.sender

    # Update battle in storage
    self.battles[_battle_index - 1] = _battle

    # Update player statuses
    self.players[self.playerInfo[_battle.players[0]]].inBattle = True
    self.players[self.playerInfo[msg.sender]].inBattle = True

    # Emit event
    log NewBattle(_battle.name, _battle.players[0], msg.sender)

    return _battle
    
@external
def attackOrDefendChoice(_choice: uint8, _battleName: String[100]):
    """
    @dev User chooses attack or defense move for battle card
    @param _choice Move choice (1 for attack, 2 for defense)
    @param _battleName Name of the battle
    """
    # Initial validations
    assert _choice == 1 or _choice == 2, "Invalid move choice"
    
    # Get battle from storage
    _battle_index: uint256 = self.battleInfo[_battleName]
    assert _battle_index != 0, "Battle doesn't exist!"
    
    # Get battle data
    _battle: Battle = self.battles[_battle_index - 1]
    
    # Battle status checks
    assert _battle.battleStatus == BattleStatus.STARTED, "Battle not started"
    assert _battle.battleStatus != BattleStatus.ENDED, "Battle has ended"
    
    # Verify player participation
    assert msg.sender == _battle.players[0] or msg.sender == _battle.players[1], "Not in battle"
    
    # Determine player index
    _player_index: uint256 = 0
    if msg.sender == _battle.players[1]:
        _player_index = 1
    
    # Check if previous round needs resolution
    if _battle.moves[0] != 0 and _battle.moves[1] != 0:
        # Previous round needs resolution
        self._awaitBattleResults(_battleName)
        # Reload battle state after resolution
        _battle = self.battles[_battle_index - 1]
    
    # Verify move hasn't been made this round
    assert _battle.moves[_player_index] == 0, "Move already made"
    
    # Register the move
    self._registerPlayerMove(_player_index, _choice, _battleName)
    
    # Get updated battle state
    _battle = self.battles[_battle_index - 1]
    
    # Calculate and check if round complete
    _moves_made: uint256 = 0
    if _battle.moves[0] != 0:
        _moves_made += 1
    if _battle.moves[1] != 0:
        _moves_made += 1
    
    # Emit move event
    log BattleMove(_battleName, _moves_made == 1)
    
    # Resolve round if both moves made
    if _moves_made == 2:
        self._awaitBattleResults(_battleName)
@external
def quitBattle(_battleName: String[100]):
    """
    @dev Allows a player to quit an ongoing battle, resulting in the other player winning
    @param _battleName Name of the battle to quit
    """
    # Get battle from storage
    _battle_index: uint256 = self.battleInfo[_battleName]
    assert self.battleInfo[_battleName] != 0, "Battle doesn't exist!"
    _battle: Battle = self.battles[_battle_index - 1]

    # Verify sender is in the battle
    assert msg.sender == _battle.players[0] or msg.sender == _battle.players[1], "You are not in this battle!"

    # Determine winner (opposite of who quit)
    if _battle.players[0] == msg.sender:
        self._endBattle(_battle.players[1], _battle)
    else:
        self._endBattle(_battle.players[0], _battle)

@external
def getBattleState(_name: String[100]) -> Battle:
    """
    @dev Get current battle state including resolution if complete
    @param _name Name of the battle to check
    @return Battle Current battle state
    """
    _battle_index: uint256 = self.battleInfo[_name]
    assert _battle_index != 0, "Battle doesn't exist!"
    return self.battles[_battle_index - 1]

@external
def getPlayerBattleState(_player: address) -> bool:
    """
    @dev Check if player is in battle
    @param _player Address of player to check
    @return bool True if player is in battle
    """
    return self.players[self.playerInfo[_player]].inBattle

@external
def checkBattleResolution(_name: String[100]) -> Battle:
    """
    @dev Check and trigger battle resolution if needed
    @param _name Name of the battle to check
    @return Battle Updated battle state
    """
    _battle_index: uint256 = self.battleInfo[_name]
    assert _battle_index != 0, "Battle doesn't exist!"
    _battle: Battle = self.battles[_battle_index - 1]
    
    if _battle.moves[0] != 0 and _battle.moves[1] != 0:
        self._awaitBattleResults(_name)
        
    return self.battles[_battle_index - 1]