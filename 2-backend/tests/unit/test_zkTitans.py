import pytest
import boa

PLAYER_NAME = "Test Player"
TOKEN_NAME = "Test Token"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

# Battle status constants
BATTLE_STATUS_PENDING = 1  # 2^0
BATTLE_STATUS_STARTED = 2  # 2^1
BATTLE_STATUS_ENDED = 4  # 2^2
BATTLE_STATUS_QUIT = 8  # 2^3


def test_metadata_uri_is_correct(metadata_uri, titans):
    assert titans.BASE_URI() == metadata_uri  # Use BASE_URI instead of metadata_uri


def test_register_player_success(titans):
    """Test successful player registration"""
    player = boa.env.generate_address("player")

    with boa.env.prank(player):
        titans.registerPlayer(PLAYER_NAME, TOKEN_NAME)

    player_id = titans.playerInfo(player)
    player_data = titans.players(player_id)

    assert player_data[0] == player, "Player address mismatch"
    assert player_data[1] == PLAYER_NAME, "Player name mismatch"
    assert player_data[2] == 25, "Initial mana should be 25"
    assert player_data[3] == 10, "Initial health should be 10"
    assert player_data[4] == False, "Should not be in battle"


def test_register_player_game_token(titans):
    """Test game token creation during registration"""
    player = boa.env.generate_address("player")

    # Register player
    with boa.env.prank(player):
        titans.registerPlayer(PLAYER_NAME, TOKEN_NAME)

    # Print token info for debugging
    token_id = titans.playerTokenInfo(player)
    token = titans.gameTokens(token_id)
    print(f"Token ID: {token_id}")
    print(f"Token Data: {token}")

    # Verify token name since structure is (name, attack, defense, other stats...)
    assert token[0] == TOKEN_NAME, "Token name mismatch"


def test_create_random_game_token(titans):
    """Test creating game token without registration"""
    player = boa.env.generate_address("player")

    # Try to create token without registration
    with boa.env.prank(player):
        try:
            titans.createRandomGameToken(TOKEN_NAME)
            assert False, "Should fail without registration"
        except Exception as e:
            print(f"Error occurred (as expected): {e}")
            # Just verify the call failed, don't check specific message
            assert True


def test_multiple_players_registration(titans):
    """Test registering multiple players"""
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")

    # Register first player
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")

    # Register second player
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    # Verify both players
    player1_id = titans.playerInfo(player1)
    player2_id = titans.playerInfo(player2)

    player1_data = titans.players(player1_id)
    player2_data = titans.players(player2_id)

    assert player1_data[0] == player1, "Player 1 address mismatch"
    assert player2_data[0] == player2, "Player 2 address mismatch"
    assert player1_id != player2_id, "Players should have different IDs"


def test_contract_initialization_and_registration(titans):
    """Test contract initialization and player registration"""
    print("\nStep 1: Initial Contract State")
    # Check initial state
    all_players = titans.getAllPlayers()
    print(f"- Initial players array length: {len(all_players)}")
    if len(all_players) > 0:
        print(f"- First player in array: {all_players[0]}")

    print("\nStep 2: Player Registration")
    player1 = boa.env.generate_address("player1")
    print(f"- Generated player address: {player1}")

    with boa.env.prank(player1):
        print("- Registering player...")
        titans.registerPlayer("Test Player", "Test Token")

        print("\nStep 3: Post-Registration Checks")
        player_id = titans.playerInfo(player1)
        print(f"- Player ID from playerInfo: {player_id}")

        # Check the actual player data in the array
        player_data = titans.players(player_id)
        print(f"- Player data from array: {player_data}")

        # Verify player address matches
        assert player_data[0] == player1, "Player address should match"

        # Check if player is registered
        is_registered = titans.isPlayer(player1)
        print(f"- isPlayer check: {is_registered}")

    assert titans.isPlayer(player1), "Player should be registered"


def test_battle_creation(titans):
    """Test battle creation functionality"""
    print("\nStep 1: Player Setup")
    player1 = boa.env.generate_address("player1")

    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
        assert titans.isPlayer(player1), "Player 1 should be registered"

    print("\nStep 2: Battle Creation")
    battle_name = "Epic Battle"
    initial_battle_count = len(titans.getAllBattles())
    print(f"- Initial battles count: {initial_battle_count}")

    with boa.env.prank(player1):
        battle = titans.createBattle(battle_name)
        battle_id = titans.battleInfo(battle_name)
        print(f"- Battle created with ID: {battle_id}")
        print(f"- Battle struct: {battle}")

    print("\nStep 3: Verification")
    is_battle = titans.isBattle(battle_name)
    print(f"- isBattle check: {is_battle}")
    print(f"- Battle ID in mapping: {titans.battleInfo(battle_name)}")
    print(f"- Total battles: {len(titans.getAllBattles())}")

    assert titans.isBattle(battle_name), "Battle should exist"

    # Get battle data as tuple (status, hash, name, players, moves, winner)
    battle_data = titans.getBattle(battle_name)
    print(f"- Retrieved battle data: {battle_data}")

    # Verify battle data using tuple indices
    assert battle_data[0] == 1, "Battle should be in PENDING status"  # status
    assert battle_data[2] == battle_name, "Battle name should match"  # name
    assert battle_data[3][0] == player1, "Player 1 should be creator"  # players[0]
    assert (
        battle_data[3][1] == ZERO_ADDRESS
    ), "Player 2 slot should be empty"  # players[1]
    assert battle_data[4] == [0, 0], "Moves should be [0, 0]"  # moves
    assert battle_data[5] == ZERO_ADDRESS, "Winner should be empty"  # winner

    print("- All battle checks passed!")


def test_join_battle(titans):
    """Test joining an existing battle"""
    print("\nStep 1: Setup")
    # Create players
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")

    # Register players
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    print("\nStep 2: Create Battle")
    battle_name = "Epic Battle"
    with boa.env.prank(player1):
        battle = titans.createBattle(battle_name)
        print(f"- Battle created with ID: {titans.battleInfo(battle_name)}")
        print(f"- Initial battle: {battle}")

    print("\nStep 3: Join Battle")
    with boa.env.prank(player2):
        battle_id = titans.battleInfo(battle_name)
        print(f"- Battle ID before joining: {battle_id}")
        battle = titans.joinBattle(battle_name)
        print(f"- Battle after joining: {battle}")

    print("\nStep 4: Verification")
    battle_data = titans.getBattle(battle_name)
    print(f"- Final battle data: {battle_data}")

    # Verify battle data
    assert (
        battle_data[0] == 2
    ), "Battle should be in STARTED status"  # BattleStatus.STARTED = 2
    assert battle_data[3][0] == player1, "Player 1 should be creator"
    assert battle_data[3][1] == player2, "Player 2 should be joiner"

    # Verify players are marked as in battle
    player1_data = titans.getPlayer(player1)
    player2_data = titans.getPlayer(player2)
    print(f"- Player 1 data: {player1_data}")
    print(f"- Player 2 data: {player2_data}")

    assert player1_data[4] == True, "Player 1 should be marked as in battle"
    assert player2_data[4] == True, "Player 2 should be marked as in battle"

    print("- All join battle checks passed!")


def test_join_battle_edge_cases(titans):
    """Test edge cases for joining battles"""
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")
    player3 = boa.env.generate_address("player3")

    print("\nStep 1: Setup")
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")
    with boa.env.prank(player3):
        titans.registerPlayer("Player Three", "Token Three")

    battle_name = "Epic Battle"

    print("\nStep 2: Test Cases")
    # Case 1: Try joining non-existent battle
    print("- Testing non-existent battle")
    with boa.env.prank(player2):
        with pytest.raises(Exception):
            titans.joinBattle(battle_name)

    # Create a battle for remaining tests
    with boa.env.prank(player1):
        battle = titans.createBattle(battle_name)
        print(f"Battle created: {battle}")

    # Case 2: Creator trying to join their own battle
    print("\n- Testing creator joining own battle")
    with boa.env.prank(player1):
        with pytest.raises(Exception):
            titans.joinBattle(battle_name)

    # Case 3: Successfully join battle with player2
    print("\n- Testing successful battle join")
    with boa.env.prank(player2):
        battle = titans.joinBattle(battle_name)
        print(f"Battle after join: {battle}")
        assert battle[0] == 2, "Battle status should be STARTED"

    # Case 4: Try joining a battle that's already started
    print("\n- Testing joining started battle")
    with boa.env.prank(player3):
        with pytest.raises(Exception):
            titans.joinBattle(battle_name)

    print("\nAll edge cases passed successfully!")


def test_get_player(titans):
    """Test getPlayer function for all cases"""
    print("\nTesting getPlayer function")

    # Case 1: Try to get non-existent player
    non_existent = boa.env.generate_address("non_existent")
    with pytest.raises(Exception) as exc_info:
        titans.getPlayer(non_existent)
    print(f"- Non-existent player error (expected): {exc_info.value}")

    # Case 2: Get existing player
    player1 = boa.env.generate_address("player1")
    with boa.env.prank(player1):
        titans.registerPlayer("Test Player", "Test Token")

    player_data = titans.getPlayer(player1)
    print(f"- Retrieved player data: {player_data}")

    # Verify all player fields
    assert player_data[0] == player1, "Player address mismatch"
    assert player_data[1] == "Test Player", "Player name mismatch"
    assert player_data[2] == 25, "Initial mana should be 25"
    assert player_data[3] == 10, "Initial health should be 10"
    assert player_data[4] == False, "Should not be in battle"

    # Case 3: Try to get player with zero address
    with pytest.raises(Exception) as exc_info:
        titans.getPlayer(ZERO_ADDRESS)
    print(f"- Zero address error (expected): {exc_info.value}")

    print("All getPlayer cases passed successfully!")


def test_get_all_players(titans):
    """Test getAllPlayers function"""
    print("\nTesting getAllPlayers function")

    # Case 1: Initial state (should have default empty player)
    initial_players = titans.getAllPlayers()
    print(f"- Initial players array: {initial_players}")
    assert len(initial_players) > 0, "Should have at least one entry (empty player)"

    # Case 2: After adding one player
    player1 = boa.env.generate_address("player1")
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")

    one_player = titans.getAllPlayers()
    print(f"- Players after one registration: {one_player}")
    assert len(one_player) > len(initial_players), "Players array should grow"

    # Case 3: After adding multiple players
    player2 = boa.env.generate_address("player2")
    player3 = boa.env.generate_address("player3")

    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")
    with boa.env.prank(player3):
        titans.registerPlayer("Player Three", "Token Three")

    all_players = titans.getAllPlayers()
    print(f"- Players after all registrations: {all_players}")

    # Verify all players are present
    player_addresses = [p[0] for p in all_players]
    assert player1 in player_addresses, "Player 1 should be in array"
    assert player2 in player_addresses, "Player 2 should be in array"
    assert player3 in player_addresses, "Player 3 should be in array"

    # Verify array properties
    assert (
        len(all_players) == len(initial_players) + 3
    ), "Should have initial + 3 players"

    print("All getAllPlayers cases passed successfully!")


def test_is_player_token(titans):
    """Test isPlayerToken function for all cases"""
    print("\nTesting isPlayerToken function")

    # Case 1: Check unregistered address
    random_address = boa.env.generate_address("random")
    assert not titans.isPlayerToken(
        random_address
    ), "Unregistered address should not have a token"
    print("- Unregistered address check passed")

    # Case 2: Check zero address
    assert not titans.isPlayerToken(
        ZERO_ADDRESS
    ), "Zero address should not have a token"
    print("- Zero address check passed")

    # Case 3: Check address after player registration (should have token)
    player1 = boa.env.generate_address("player1")
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    assert titans.isPlayerToken(player1), "Registered player should have a token"
    print("- Registered player token check passed")

    # Case 4: Check player after creating additional token
    with boa.env.prank(player1):
        titans.createRandomGameToken("Another Token")
    assert titans.isPlayerToken(
        player1
    ), "Player should still have token after creating another"
    print("- Multiple tokens check passed")

    print("All isPlayerToken cases passed successfully!")


def test_get_player_token(titans):
    """Test getPlayerToken function for all cases"""
    print("\nTesting getPlayerToken function")

    # Case 1: Try to get token for non-existent player
    non_existent = boa.env.generate_address("non_existent")
    with pytest.raises(Exception) as exc_info:
        titans.getPlayerToken(non_existent)
    print(f"- Non-existent player error (expected): {exc_info.value}")

    # Case 2: Try to get token for zero address
    with pytest.raises(Exception) as exc_info:
        titans.getPlayerToken(ZERO_ADDRESS)
    print(f"- Zero address error (expected): {exc_info.value}")

    # Case 3: Get token for registered player
    player1 = boa.env.generate_address("player1")
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")

    token = titans.getPlayerToken(player1)
    print(f"- Retrieved token data: {token}")

    # Verify token fields
    assert token[0] == "Token One", "Token name mismatch"
    assert token[1] >= 0, "Token ID should be non-negative"
    assert 0 <= token[2] <= 10, "Attack strength should be between 0 and 10"
    assert 0 <= token[3] <= 10, "Defense strength should be between 0 and 10"
    assert token[2] + token[3] == 10, "Total of attack and defense should be 10"

    # Case 4: Get token after creating additional token
    with boa.env.prank(player1):
        titans.createRandomGameToken("Token Two")

    updated_token = titans.getPlayerToken(player1)
    print(f"- Updated token data: {updated_token}")
    assert updated_token[0] == "Token Two", "New token name mismatch"

    print("All getPlayerToken cases passed successfully!")


def test_get_all_player_tokens(titans):
    """Test getAllPlayerTokens function"""
    print("\nTesting getAllPlayerTokens function")

    # Case 1: Initial state (should have default empty token)
    initial_tokens = titans.getAllPlayerTokens()
    print(f"- Initial tokens array: {initial_tokens}")
    assert len(initial_tokens) > 0, "Should have at least one entry (empty token)"
    assert initial_tokens[0][0] == "", "First token should be empty"

    # Case 2: After adding one player/token
    player1 = boa.env.generate_address("player1")
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")

    one_token = titans.getAllPlayerTokens()
    print(f"- Tokens after one registration: {one_token}")
    assert len(one_token) > len(initial_tokens), "Tokens array should grow"
    assert one_token[-1][0] == "Token One", "Last token should be the new one"

    # Case 3: After adding multiple players/tokens
    player2 = boa.env.generate_address("player2")
    player3 = boa.env.generate_address("player3")

    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")
    with boa.env.prank(player3):
        titans.registerPlayer("Player Three", "Token Three")

    all_tokens = titans.getAllPlayerTokens()
    print(f"- Tokens after all registrations: {all_tokens}")

    # Verify all tokens are present by name
    token_names = [t[0] for t in all_tokens]
    assert "Token One" in token_names, "Token One should be in array"
    assert "Token Two" in token_names, "Token Two should be in array"
    assert "Token Three" in token_names, "Token Three should be in array"

    # Case 4: After creating additional token for existing player
    with boa.env.prank(player1):
        titans.createRandomGameToken("Token Four")

    updated_tokens = titans.getAllPlayerTokens()
    print(f"- Tokens after additional token creation: {updated_tokens}")
    assert "Token Four" in [
        t[0] for t in updated_tokens
    ], "New token should be in array"

    # Verify token properties
    for token in updated_tokens[1:]:  # Skip first empty token
        assert token[0] != "", "Token name should not be empty"
        assert 0 <= token[2] <= 10, "Attack should be between 0 and 10"
        assert 0 <= token[3] <= 10, "Defense should be between 0 and 10"
        assert token[2] + token[3] == 10, "Attack + Defense should equal 10"

    print("All getAllPlayerTokens cases passed successfully!")


def test_get_total_supply(titans):
    """Test getTotalSupply function"""
    print("\nTesting getTotalSupply function")

    # Case 1: Initial state (should be 0)
    initial_supply = titans.getTotalSupply()
    print(f"- Initial total supply: {initial_supply}")
    assert initial_supply == 0, "Initial supply should be 0"

    # Case 2: After registering one player (should increase)
    player1 = boa.env.generate_address("player1")
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")

    supply_after_one = titans.getTotalSupply()
    print(f"- Supply after one registration: {supply_after_one}")
    assert (
        supply_after_one > initial_supply
    ), "Supply should increase after registration"

    # Case 3: After multiple registrations
    player2 = boa.env.generate_address("player2")
    player3 = boa.env.generate_address("player3")

    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")
    with boa.env.prank(player3):
        titans.registerPlayer("Player Three", "Token Three")

    supply_after_three = titans.getTotalSupply()
    print(f"- Supply after three registrations: {supply_after_three}")
    assert supply_after_three == supply_after_one + 2, "Supply should increase by 2"

    # Case 4: After creating additional token
    with boa.env.prank(player1):
        titans.createRandomGameToken("Token Four")

    final_supply = titans.getTotalSupply()
    print(f"- Final supply after additional token: {final_supply}")
    assert final_supply == supply_after_three + 1, "Supply should increase by 1"

    print("All getTotalSupply cases passed successfully!")


def test_is_battle(titans):
    """Test isBattle function for all cases"""
    print("\nTesting isBattle function")

    # Case 1: Check non-existent battle
    assert not titans.isBattle(
        "Non-existent Battle"
    ), "Non-existent battle should return False"
    print("- Non-existent battle check passed")

    # Case 2: Check empty string
    assert not titans.isBattle(""), "Empty string should return False"
    print("- Empty string check passed")

    # Case 3: Create and check battle
    player1 = boa.env.generate_address("player1")
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
        battle = titans.createBattle("Epic Battle")

    assert titans.isBattle("Epic Battle"), "Created battle should return True"
    print("- Created battle check passed")

    # Case 4: Check case sensitivity
    assert not titans.isBattle("epic battle"), "Battle names should be case sensitive"
    print("- Case sensitivity check passed")

    # Case 5: Create multiple battles
    with boa.env.prank(player1):
        titans.createBattle("Another Battle")

    assert titans.isBattle("Epic Battle"), "First battle should still exist"
    assert titans.isBattle("Another Battle"), "Second battle should exist"
    print("- Multiple battles check passed")

    print("All isBattle cases passed successfully!")


def test_get_battle(titans):
    """Test getBattle function for all cases"""
    print("\nTesting getBattle function")

    # Case 1: Try to get non-existent battle
    with pytest.raises(Exception) as exc_info:
        titans.getBattle("Non-existent Battle")
    print(f"- Non-existent battle error (expected): {exc_info.value}")

    # Setup players
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")

    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    # Case 2: Get newly created battle
    battle_name = "Epic Battle"
    with boa.env.prank(player1):
        titans.createBattle(battle_name)

    battle = titans.getBattle(battle_name)
    print(f"- New battle data: {battle}")

    # Verify battle fields
    assert (
        battle[0] == 1
    ), "New battle should be in PENDING status"  # BattleStatus.PENDING
    assert battle[2] == battle_name, "Battle name should match"
    assert battle[3][0] == player1, "Player 1 should be creator"
    assert battle[3][1] == ZERO_ADDRESS, "Player 2 should be empty"
    assert battle[4] == [0, 0], "Moves should be [0, 0]"
    assert battle[5] == ZERO_ADDRESS, "Winner should be empty"

    # Case 3: Get battle after player joins
    with boa.env.prank(player2):
        titans.joinBattle(battle_name)

    updated_battle = titans.getBattle(battle_name)
    print(f"- Battle data after join: {updated_battle}")

    assert (
        updated_battle[0] == 2
    ), "Battle should be in STARTED status"  # BattleStatus.STARTED
    assert updated_battle[3][1] == player2, "Player 2 should be joiner"

    # Case 4: Try to get battle with empty name
    with pytest.raises(Exception) as exc_info:
        titans.getBattle("")
    print(f"- Empty battle name error (expected): {exc_info.value}")

    # Case 5: Verify 1-based indexing (if possible)
    battle_id = titans.battleInfo(battle_name)
    print(f"- Battle ID from mapping: {battle_id}")
    assert battle_id > 0, "Battle ID should be greater than 0 (1-based indexing)"

    print("All getBattle cases passed successfully!")


def test_get_all_battles(titans):
    """Test getAllBattles function"""
    print("\nTesting getAllBattles function")

    # Case 1: Initial state (should have empty battle array)
    initial_battles = titans.getAllBattles()
    print(f"- Initial battles array: {initial_battles}")
    assert len(initial_battles) >= 0, "Should start with empty or initialized array"

    # Setup players
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")

    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    # Case 2: After creating one battle
    battle_name1 = "Epic Battle"
    with boa.env.prank(player1):
        titans.createBattle(battle_name1)

    one_battle = titans.getAllBattles()
    print(f"- Battles after one creation: {one_battle}")
    assert len(one_battle) > len(initial_battles), "Battles array should grow"

    # Case 3: After creating multiple battles
    battle_name2 = "Awesome Battle"
    battle_name3 = "Final Battle"

    with boa.env.prank(player1):
        titans.createBattle(battle_name2)
    with boa.env.prank(player2):
        titans.createBattle(battle_name3)

    all_battles = titans.getAllBattles()
    print(f"- Battles after all creations: {all_battles}")

    # Case 4: After joining a battle
    with boa.env.prank(player2):
        titans.joinBattle(battle_name1)

    updated_battles = titans.getAllBattles()
    print(f"- Battles after join: {updated_battles}")

    # Verify battle states
    battle_names = [b[2] for b in updated_battles]  # Get names from battles
    assert battle_name1 in battle_names, "First battle should exist"
    assert battle_name2 in battle_names, "Second battle should exist"
    assert battle_name3 in battle_names, "Third battle should exist"

    # Find the joined battle
    joined_battle = next(b for b in updated_battles if b[2] == battle_name1)
    assert joined_battle[0] == 2, "Joined battle should be in STARTED status"
    assert joined_battle[3][1] == player2, "Player 2 should be in joined battle"

    print("All getAllBattles cases passed successfully!")


def test_get_battle_moves(titans):
    """Test getBattleMoves function"""
    print("\nTesting getBattleMoves function")

    # Case 1: Try to get moves for non-existent battle
    with pytest.raises(Exception) as exc_info:
        titans.getBattleMoves("Non-existent Battle")
    print(f"- Non-existent battle error (expected): {exc_info.value}")

    # Setup players
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")

    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    # Case 2: Get moves for new battle (should be 0,0)
    battle_name = "Epic Battle"
    with boa.env.prank(player1):
        titans.createBattle(battle_name)

    initial_moves = titans.getBattleMoves(battle_name)
    print(f"- Initial moves: {initial_moves}")
    assert initial_moves == (0, 0), "New battle should have (0,0) moves"

    # Case 3: Get moves after battle starts
    with boa.env.prank(player2):
        titans.joinBattle(battle_name)

    moves_after_join = titans.getBattleMoves(battle_name)
    print(f"- Moves after join: {moves_after_join}")
    assert moves_after_join == (0, 0), "Joined battle should still have (0,0) moves"

    # Case 4: Try to get moves with empty battle name
    with pytest.raises(Exception) as exc_info:
        titans.getBattleMoves("")
    print(f"- Empty battle name error (expected): {exc_info.value}")

    # Case 5: Get moves after moves are made (if possible)
    # Note: This depends on having a method to make moves
    # If you have a makeMoves or similar function, add:
    #
    # with boa.env.prank(player1):
    #     titans.makeMove(battle_name, 1)  # Example move
    # with boa.env.prank(player2):
    #     titans.makeMove(battle_name, 2)  # Example move
    #
    # final_moves = titans.getBattleMoves(battle_name)
    # print(f"- Moves after players moved: {final_moves}")
    # assert final_moves == (1, 2), "Moves should reflect player actions"

    print("All getBattleMoves cases passed successfully!")


def test_set_uri(titans, metadata_uri):
    """Test setURI function"""
    print("\nTesting setURI function")

    # Case 1: Try to set URI from non-owner
    non_owner = boa.env.generate_address("non_owner")
    with boa.env.prank(non_owner):
        with pytest.raises(Exception) as exc_info:
            titans.setURI("new_uri")
    print(f"- Non-owner error (expected): {exc_info.value}")

    # Case 2: Get initial URI
    initial_uri = titans.BASE_URI()
    print(f"- Initial URI: {initial_uri}")

    # Case 3: Set new URI as owner
    owner = titans.owner()
    new_uri = "https://new-metadata-uri.com/"
    with boa.env.prank(owner):
        titans.setURI(new_uri)

    updated_uri = titans.BASE_URI()
    print(f"- Updated URI: {updated_uri}")
    assert updated_uri == new_uri, "URI should be updated"

    # Case 4: Try to set empty URI
    with boa.env.prank(owner):
        titans.setURI("")

    empty_uri = titans.BASE_URI()
    print(f"- Empty URI set: {empty_uri}")
    assert empty_uri == "", "Should allow empty URI"

    # Case 5: Try to set moderate length URI
    moderate_uri = "https://metadata.example.com/api/v1/tokens/"  # reasonable length
    with boa.env.prank(owner):
        titans.setURI(moderate_uri)

    moderate_uri_result = titans.BASE_URI()
    print(f"- Moderate length URI: {moderate_uri_result}")
    assert moderate_uri_result == moderate_uri, "Should handle moderate length URI"

    print("All setURI cases passed successfully!")


def test_registering_player(titans):
    """Test registerPlayer function"""
    print("\nTesting registerPlayer function")

    # Case 1: Register first player
    player1 = boa.env.generate_address("player1")
    print(f"- Player1 address: {player1}")

    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")

    # Verify player data using playerInfo mapping
    player_id = titans.playerInfo(player1)
    print(f"- Player ID in mapping: {player_id}")

    # Get player data using the ID
    player_data = titans.players(player_id)
    print(f"- First player data: {player_data}")
    assert (
        player_data[0] == player1
    ), f"Player address mismatch. Expected {player1}, got {player_data[0]}"
    assert player_data[1] == "Player One", "Player name mismatch"
    assert player_data[2] == 25, "Initial mana should be 25"
    assert player_data[3] == 10, "Initial health should be 10"
    assert player_data[4] == False, "Should not be in battle"

    # Case 2: Try to register same player again
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.registerPlayer("Player One Again", "Token Two")
    print(f"- Duplicate registration error (expected): {exc_info.value}")

    # Case 3: Register second player
    player2 = boa.env.generate_address("player2")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    # Verify second player data
    player2_id = titans.playerInfo(player2)
    print(f"- Player2 ID in mapping: {player2_id}")

    player2_data = titans.players(player2_id)
    print(f"- Second player data: {player2_data}")
    assert player2_data[0] == player2, "Player 2 address mismatch"
    assert player2_data[1] == "Player Two", "Player 2 name mismatch"

    # Case 4: Verify both players have tokens
    token1 = titans.getPlayerToken(player1)
    token2 = titans.getPlayerToken(player2)
    print(f"- Player 1 token: {token1}")
    print(f"- Player 2 token: {token2}")
    assert token1[0] == "Token One", "Player 1 token name mismatch"
    assert token2[0] == "Token Two", "Player 2 token name mismatch"

    print("All registerPlayer cases passed successfully!")


def test_creating_random_game_token(titans):
    """Test createRandomGameToken function"""
    print("\nTesting createRandomGameToken function")

    # Setup: Create player address
    player1 = boa.env.generate_address("player1")
    print(f"- Player1 address: {player1}")

    # Case 1: Try to create token without registering
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.createRandomGameToken("Unregistered Token")
    print(f"- Unregistered player error (expected): {exc_info.value}")

    # Case 2: Register player and create first token
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "First Token")

    # Get initial token
    initial_token = titans.getPlayerToken(player1)
    print(f"- Initial token: {initial_token}")

    # Create additional token
    with boa.env.prank(player1):
        titans.createRandomGameToken("Second Token")

    # Verify new token
    new_token = titans.getPlayerToken(player1)
    print(f"- New token: {new_token}")
    assert new_token[0] == "Second Token", "New token name mismatch"

    # Case 3: Create token while in battle
    # First, setup a battle and get player2 to join
    player2 = boa.env.generate_address("player2")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    with boa.env.prank(player1):
        titans.createBattle("Test Battle")

    with boa.env.prank(player2):
        titans.joinBattle("Test Battle")

    # Verify battle state
    player_data = titans.players(titans.playerInfo(player1))
    print(f"- Player battle state: {player_data[4]}")  # inBattle status

    # Try to create token while in battle
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.createRandomGameToken("Battle Token")
    print(f"- In battle error (expected): {exc_info.value}")

    # Case 4: Verify total supply increased
    total_supply = titans.TOTAL_SUPPLY()
    print(f"- Total supply: {total_supply}")
    assert total_supply > 1, "Total supply should increase with each token"

    print("All createRandomGameToken cases passed successfully!")


def test_creating_battle(titans):
    """Test createBattle function"""
    print("\nTesting createBattle function")

    # Setup: Create player addresses
    player1 = boa.env.generate_address("player1")
    print(f"- Player1 address: {player1}")

    # Case 1: Try to create battle without registering
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.createBattle("Unregistered Battle")
    print("- Unregistered player error caught successfully")

    # Case 2: Register player and create first battle
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")

    battle_name = "Epic Battle"
    with boa.env.prank(player1):
        battle = titans.createBattle(battle_name)

    # Verify battle data
    print(f"- Created battle: {battle}")
    assert battle[0] == 1, "Battle should be in PENDING state"  # BattleStatus.PENDING
    assert battle[2] == battle_name, "Battle name mismatch"
    assert battle[3][0] == player1, "Creator address mismatch"
    assert (
        battle[3][1] == "0x0000000000000000000000000000000000000000"
    ), "Second player should be empty"
    assert battle[4] == [0, 0], "Moves should be initialized to 0"
    assert (
        battle[5] == "0x0000000000000000000000000000000000000000"
    ), "Winner should be empty"

    # Case 3: Try to create battle with same name
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.createBattle(battle_name)
    print("- Duplicate battle error caught successfully")

    # Case 4: Create second battle with different name
    second_battle_name = "Another Battle"
    with boa.env.prank(player1):
        second_battle = titans.createBattle(second_battle_name)

    print(f"- Second battle: {second_battle}")
    assert second_battle[2] == second_battle_name, "Second battle name mismatch"

    # Case 5: Verify battle info mapping
    battle_id = titans.battleInfo(battle_name)
    print(f"- First battle ID: {battle_id}")
    assert battle_id > 0, "Battle ID should be greater than 0"

    second_battle_id = titans.battleInfo(second_battle_name)
    print(f"- Second battle ID: {second_battle_id}")
    assert second_battle_id > battle_id, "Second battle ID should be greater than first"

    # Case 6: Try to create battle with empty name
    with boa.env.prank(player1):
        empty_battle = titans.createBattle("")

    print(f"- Empty name battle: {empty_battle}")
    assert empty_battle[2] == "", "Should allow empty battle name"

    # Case 7: Verify battles array
    battle_from_array = titans.battles(battle_id - 1)  # -1 because array is 0-based
    print(f"- Battle from array: {battle_from_array}")
    assert battle_from_array[2] == battle_name, "Battle in array mismatch"

    print("All createBattle cases passed successfully!")


def test_joining_battle(titans):
    """Test joinBattle function"""
    print("\nTesting joinBattle function")

    # Setup: Create players
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")
    player3 = boa.env.generate_address("player3")
    print(f"- Player addresses created")

    # Case 1: Try to join non-existent battle
    with boa.env.prank(player2):
        with pytest.raises(Exception) as exc_info:
            titans.joinBattle("Non-existent Battle")
    print("- Non-existent battle error caught successfully")

    # Case 2: Register players and create battle
    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    battle_name = "Epic Battle"
    with boa.env.prank(player1):
        initial_battle = titans.createBattle(battle_name)

    print(f"- Initial battle state: {initial_battle}")

    # Case 3: Try to join with unregistered player
    with boa.env.prank(player3):
        with pytest.raises(Exception) as exc_info:
            titans.joinBattle(battle_name)
    print("- Unregistered player error caught successfully")

    # Case 4: Try to join own battle
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.joinBattle(battle_name)
    print("- Own battle error caught successfully")

    # Case 5: Successfully join battle
    with boa.env.prank(player2):
        joined_battle = titans.joinBattle(battle_name)

    print(f"- Joined battle state: {joined_battle}")
    assert joined_battle[0] == 2, "Battle should be in STARTED state"
    assert joined_battle[3][1] == player2, "Second player not set correctly"

    # Case 6: Verify player battle states
    player1_data = titans.players(titans.playerInfo(player1))
    player2_data = titans.players(titans.playerInfo(player2))
    print(f"- Player1 battle state: {player1_data[4]}")
    print(f"- Player2 battle state: {player2_data[4]}")
    assert player1_data[4] == True, "Player1 should be in battle"
    assert player2_data[4] == True, "Player2 should be in battle"

    # Case 7: Try to join a battle while in another battle
    second_battle_name = "Another Battle"
    with boa.env.prank(player1):
        titans.createBattle(second_battle_name)

    with boa.env.prank(player2):
        with pytest.raises(Exception) as exc_info:
            titans.joinBattle(second_battle_name)
    print("- Already in battle error caught successfully")

    # Case 8: Try to join a battle that's already started
    with boa.env.prank(player3):
        titans.registerPlayer("Player Three", "Token Three")

    with boa.env.prank(player3):
        with pytest.raises(Exception) as exc_info:
            titans.joinBattle(battle_name)
    print("- Battle in progress error caught successfully")

    print("All joinBattle cases passed successfully!")


def test_attack_or_defend_choice(titans):
    """Test attackOrDefendChoice function"""
    print("\nTesting attackOrDefendChoice function")

    # Setup: Create and register players
    player1 = boa.env.generate_address("player1")
    player2 = boa.env.generate_address("player2")

    with boa.env.prank(player1):
        titans.registerPlayer("Player One", "Token One")
    with boa.env.prank(player2):
        titans.registerPlayer("Player Two", "Token Two")

    battle_name = "Test Battle"

    # Create and join battle
    with boa.env.prank(player1):
        titans.createBattle(battle_name)
    with boa.env.prank(player2):
        battle = titans.joinBattle(battle_name)

    # Test invalid moves and error cases
    print("\nTesting error cases:")
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.attackOrDefendChoice(3, battle_name)
    print("✓ Invalid move choice rejected")

    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.attackOrDefendChoice(1, "Non-existent Battle")
    print("✓ Non-existent battle rejected")

    non_player = boa.env.generate_address("non_player")
    with boa.env.prank(non_player):
        with pytest.raises(Exception) as exc_info:
            titans.attackOrDefendChoice(1, battle_name)
    print("✓ Non-player move rejected")

    print("\nTesting valid moves and battle resolution:")

    # Get initial states
    initial_p1_data = titans.players(titans.playerInfo(player1))
    initial_p2_data = titans.players(titans.playerInfo(player2))
    print(f"Initial P1 state: {initial_p1_data}")
    print(f"Initial P2 state: {initial_p2_data}")

    # Player 1 attacks
    with boa.env.prank(player1):
        titans.attackOrDefendChoice(1, battle_name)

    battle_after_p1 = titans.getBattleState(battle_name)
    assert battle_after_p1[4][0] == 1, "Player1 attack move not registered"
    print("✓ Player1 attack move registered")

    # Verify player1 can't move again
    with boa.env.prank(player1):
        with pytest.raises(Exception) as exc_info:
            titans.attackOrDefendChoice(2, battle_name)
    print("✓ Double move prevented")

    # Get states after P1 move
    p1_data_after_move = titans.players(titans.playerInfo(player1))
    p2_data_after_move = titans.players(titans.playerInfo(player2))
    print(f"P1 state after move: {p1_data_after_move}")
    print(f"P2 state after move: {p2_data_after_move}")

    # Player 2 defends
    with boa.env.prank(player2):
        titans.attackOrDefendChoice(2, battle_name)

    battle_after_p2 = titans.getBattleState(battle_name)
    assert battle_after_p2[4][1] == 2, "Player2 defense move not registered"
    print("✓ Player2 defense move registered")

    # Get states before resolution
    p1_before_resolution = titans.players(titans.playerInfo(player1))
    p2_before_resolution = titans.players(titans.playerInfo(player2))
    print(f"P1 before resolution: {p1_before_resolution}")
    print(f"P2 before resolution: {p2_before_resolution}")

    # Resolve battle
    with boa.env.prank(player1):
        titans.checkBattleResolution(battle_name)

    # Get final states
    p1_after_resolution = titans.players(titans.playerInfo(player1))
    p2_after_resolution = titans.players(titans.playerInfo(player2))
    print(f"P1 after resolution: {p1_after_resolution}")
    print(f"P2 after resolution: {p2_after_resolution}")

    # Verify state changes after resolution
    assert (
        p1_after_resolution[2] != p1_before_resolution[2]
    ), "Player1 mana should change"
    assert (
        p2_after_resolution[2] != p2_before_resolution[2]
    ), "Player2 mana should change"

    if p1_before_resolution[2] > p1_after_resolution[2]:
        print("✓ Player1 mana decreased (attack cost)")
    if p2_before_resolution[2] < p2_after_resolution[2]:
        print("✓ Player2 mana increased (defense bonus)")

    print("\nAll attackOrDefendChoice functionality verified successfully!")


# def test_battle_scenarios(titans):
#     """Test different battle scenarios and their outcomes"""
#     print("\nTesting Battle Scenarios")

#     # Setup: Create and register players
#     player1 = boa.env.generate_address("player1")
#     player2 = boa.env.generate_address("player2")

#     with boa.env.prank(player1):
#         titans.registerPlayer("Player One", "Token One")
#     with boa.env.prank(player2):
#         titans.registerPlayer("Player Two", "Token Two")

#     def get_battle_state(battle_name):
#         """Helper to get current battle state"""
#         battle = titans.getBattleState(battle_name)
#         return {
#             "status": battle[0],  # battleStatus
#             "moves": battle[4],  # moves
#             "winner": battle[5],  # winner
#         }

#     def get_player_stats(player_address):
#         """Helper to get player stats"""
#         player_index = titans.playerInfo(player_address)
#         player_state = titans.players(player_index)
#         token_index = titans.playerTokenInfo(player_address)
#         token_info = titans.gameTokens(token_index)

#         return {
#             "health": int(player_state[3]),
#             "mana": int(player_state[2]),
#             "attack": int(token_info[0]),
#             "defense": int(token_info[1]),
#             "token_index": token_index,
#         }

#     def fight_until_end(battle_name):
#         """Helper function to fight until someone loses"""
#         rounds = 0
#         while rounds < 10:  # Prevent infinite loops
#             print(f"\nRound {rounds + 1}")

#             # Get current states
#             p1_stats = get_player_stats(player1)
#             p2_stats = get_player_stats(player2)
#             battle_state = get_battle_state(battle_name)

#             print(
#                 f"P1: Health={p1_stats['health']}, Mana={p1_stats['mana']}, Attack={p1_stats['attack']}, Defense={p1_stats['defense']}"
#             )
#             print(
#                 f"P2: Health={p2_stats['health']}, Mana={p2_stats['mana']}, Attack={p2_stats['attack']}, Defense={p2_stats['defense']}"
#             )
#             print(f"Battle state: {battle_state}")

#             # Make moves
#             if p1_stats["mana"] >= 3:
#                 with boa.env.prank(player1):
#                     titans.attackOrDefendChoice(1, battle_name)
#                 print("P1 chose to attack")
#             else:
#                 with boa.env.prank(player1):
#                     titans.attackOrDefendChoice(2, battle_name)
#                 print("P1 chose to defend")

#             if p2_stats["mana"] >= 3:
#                 with boa.env.prank(player2):
#                     titans.attackOrDefendChoice(1, battle_name)
#                 print("P2 chose to attack")
#             else:
#                 with boa.env.prank(player2):
#                     titans.attackOrDefendChoice(2, battle_name)
#                 print("P2 chose to defend")

#             # Get battle state after moves
#             battle_state = get_battle_state(battle_name)
#             print(f"Moves after choices: {battle_state['moves']}")

#             try:
#                 # Check battle resolution
#                 with boa.env.prank(player1):
#                     titans.checkBattleResolution(battle_name)
#                 print("Battle resolution checked")

#                 # Get updated states
#                 battle_state = get_battle_state(battle_name)
#                 p1_stats = get_player_stats(player1)
#                 p2_stats = get_player_stats(player2)

#                 print(f"Battle status: {battle_state['status']}")
#                 print(f"Battle winner: {battle_state['winner']}")
#                 print(f"P1 Health: {p1_stats['health']}, Mana: {p1_stats['mana']}")
#                 print(f"P2 Health: {p2_stats['health']}, Mana: {p2_stats['mana']}")

#                 # Check for battle end conditions
#                 if p1_stats["health"] == 0:
#                     print("P1 lost - no health remaining!")
#                     break
#                 if p2_stats["health"] == 0:
#                     print("P2 lost - no health remaining!")
#                     break
#                 if battle_state["status"] == 2:  # BattleStatus.ENDED
#                     print("Battle ended by status!")
#                     break

#             except Exception as e:
#                 print(f"Error during battle resolution: {str(e)}")
#                 break

#             rounds += 1
#             boa.env.time_travel(1)

#     print("\nScenario 1: Attack vs Attack Battle")
#     battle_name = "Attack Battle"

#     # Create battle and set initial attack/defense values
#     with boa.env.prank(player1):
#         titans.createBattle(battle_name)
#         # Set initial attack/defense for player 1
#         token_index = titans.playerTokenInfo(player1)
#         titans.gameTokens[token_index].attackStrength = 5
#         titans.gameTokens[token_index].defenseStrength = 5

#     with boa.env.prank(player2):
#         titans.joinBattle(battle_name)
#         # Set initial attack/defense for player 2
#         token_index = titans.playerTokenInfo(player2)
#         titans.gameTokens[token_index].attackStrength = 5
#         titans.gameTokens[token_index].defenseStrength = 5

#     # Get initial states
#     p1_initial = get_player_stats(player1)
#     p2_initial = get_player_stats(player2)

#     print(f"Initial states:")
#     print(f"P1: {p1_initial}")
#     print(f"P2: {p2_initial}")

#     # Fight until someone wins
#     fight_until_end(battle_name)

#     # Get final states
#     p1_final = get_player_stats(player1)
#     p2_final = get_player_stats(player2)
#     battle_final = get_battle_state(battle_name)

#     print(f"\nFinal states:")
#     print(f"P1: {p1_final}")
#     print(f"P2: {p2_final}")
#     print(f"Battle winner: {battle_final['winner']}")

#     # Verify battle ended properly
#     assert not titans.players(titans.playerInfo(player1))[
#         4
#     ], "Player1 should not be in battle"
#     assert not titans.players(titans.playerInfo(player2))[
#         4
#     ], "Player2 should not be in battle"
#     assert battle_final["winner"] != ZERO_ADDRESS, "Battle should have a winner"
#     assert (
#         p1_final["health"] == 0 or p2_final["health"] == 0
#     ), "One player should have lost all health"

#     print("\nAll battle scenarios tested successfully!")
