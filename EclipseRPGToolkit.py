import random
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------Weapon Class--------------------------------
class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    # Clone method to create a new object with the same attributes
    def clone(self):
        return Weapon(self.name, self.damage)


# Load weapons from Weapons.txt
weapons = []
weapon_lookup = {}  # Dictionary for quick access by name

weapons_path = os.path.join(script_dir, 'Weapons.txt')
with open(weapons_path, 'r') as file:
    for line in file:
        name, damage = line.strip().split(',')
        weapon = Weapon(name, int(damage))
        weapons.append(weapon)  # Store in the list
        weapon_lookup[name.lower().replace(" ", "_")] = weapon  # Store in dictionary


# -------------------------------Armor Class---------------------------------
class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

    # Clone method to create a new object with the same attributes
    def clone(self):
        return Armor(self.name, self.defense)


# Load armor from Armors.txt
armors = []
armor_lookup = {}

armors_path = os.path.join(script_dir, 'Armors.txt')
with open(armors_path, 'r') as file:
    for line in file:
        name, defense = line.strip().split(',')
        armor = Armor(name, int(defense))
        armors.append(armor)  # Store in the list
        armor_lookup[name.lower().replace(" ", "_")] = armor  # Store in dictionary


# -------------------------------Item Class---------------------------------
class Item:
    def __init__(self, name, healthgain):
        self.name = name
        self.heal = healthgain

    # Clone method to create a new object with the same attributes
    def clone(self):
        return Item(self.name, self.heal)


# Load items from Items.txt
items = []
item_lookup = {}

items_path = os.path.join(script_dir, 'Items.txt')
with open(items_path, 'r') as file:
    for line in file:
        name, heal = line.strip().split(',')
        item = Item(name, int(heal))
        items.append(item)  # Store in the list
        item_lookup[name.lower().replace(" ", "_")] = item  # Store in dictionary

# -------------------------------Player Class--------------------------------
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 5
        self.armor = None
        self.weapon = None
        self.inventory = [armor_lookup["leather_armor"], item_lookup["small_healing_potion"], weapon_lookup["dagger"]]
        self.gold = 0

    def equip_weapon(self, weapon):
        if weapon in self.inventory:
            self.weapon = weapon
            self.inventory.remove(weapon)
            print(f"{self.name} equipped {weapon.name}!")
        else:
            print(f"{weapon.name} is not in your inventory!")

    def equip_armor(self, armor):
        if armor in self.inventory:
            self.armor = armor
            self.inventory.remove(armor)
            print(f"{self.name} equipped {armor.name}!")
        else:
            print(f"{armor.name} is not in your inventory!")

    def attack(self, enemy):
        damage = self.attack_power + (self.weapon.damage if self.weapon else 0)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

    def take_damage(self, damage):
        reduced_damage = damage - (self.armor.defense if self.armor else 0)
        self.health -= max(reduced_damage, 0)
        print(f"{self.name} took {reduced_damage} damage! Health: {self.health}")


# -------------------------------------Enemy Class-----------------------------------------
class Enemy:
    enemy_lookup = {}  # Dictionary for quick lookup

    def __init__(self, name, health, attack_power, goldDrop, diffRating):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.goldDrop = goldDrop
        self.diffRating = diffRating

    def take_damage(self, damage):
        self.health -= damage
        if self.health > 0:
            print(f"{self.name} took {damage} damage! Health left: {self.health}")
        else:
            print(f"{self.name} was defeated!")

    def attack(self, player):
        print(f"{self.name} attacks {player.name} for {self.attack_power} damage!")
        player.take_damage(self.attack_power)

    @classmethod
    def load_enemies(cls, file_path):
        """Loads enemies from a file and populates the lookup dictionary."""
        with open(file_path, 'r') as file:
            for line in file:
                name, health, attack_power, goldDrop, diffRating = line.strip().split(',')
                cls.enemy_lookup[name.lower().replace(" ", "_")] = (name, int(health), int(attack_power), int(goldDrop), int(diffRating))

    @classmethod
    def get_random_enemy(cls, difficulty):
        """Creates a fresh instance of a random enemy, applying difficulty scaling."""
        # Map difficulty to the corresponding diffRating
        difficulty_rating = {"easy": 1, "medium": 2, "hard": 3}[difficulty]

        # Filter enemies by difficulty rating
        filtered_enemies = [enemy for enemy in cls.enemy_lookup.values() if enemy[4] == difficulty_rating]

        if not filtered_enemies:
            raise ValueError(f"No enemies found for difficulty: {difficulty}")

        # Select a random enemy from the filtered list
        name, base_health, base_attack, goldDrop, diffRating = random.choice(filtered_enemies)

        return cls(name, base_health, base_attack, goldDrop, diffRating)



# -------------------------------Game Setup---------------------------------
playername = input("Please enter your name: ")
player = Player(playername)
counter = 0
difficulty = "easy"

shopCountdown = 0
shopCounter = 0

trapRoomCountdown = 0
trapRoomCounter = 0
combatCounter = 0
# Start game
print(f"You have {player.health} HP.")


# -------------------------------Main Rest Menu--------------------------------
def rest(player, enemy):
    global trapRoomCounter, shopCounter
    if trapRoomCounter == 0:
        trapRoomCounter = random.randint(6, 10)
    if shopCounter == 0:
        shopCounter = random.randint(3, 10)
    if trapRoomCounter == shopCounter:
        trapRoomCounter += 3

    restchoice = input("Please choose a following option:[1] Enter Fight [2] View Inventory [3] Equip Gear [4] Use Item [5] View Player Stats [6] Debug Info: ")
    if restchoice == "1":
        player_turn(player, enemy)

    elif restchoice == "2":
        print("Inventory:")
        for item in player.inventory:
            print(f"- {item.name}")
        print(f"Gold: {player.gold}")
        rest(player, enemy)

    elif restchoice == "3":
        equip_gear(player)
        rest(player, enemy)

    elif restchoice == "4":
        use_item(player)
        rest(player, enemy)

    elif restchoice == "5":
        print(f"""
        ==========================
        |      Player Stats      |
        ==========================
        | Name: {player.name}
        | Health: {player.health}
        | Attack Power: {player.attack_power} + {player.weapon.damage if player.weapon else 0}
        | Weapon: {player.weapon.name if player.weapon else 'None'}
        | Armor: {player.armor.name if player.armor else 'None'}
        | Defense: {player.armor.defense if player.armor else 0}
        | Gold: {player.gold}
        ==========================
        """)
        rest(player, enemy)

    elif restchoice == "6":
        debug(player, enemy)
    else:
        print("Invalid action. Please choose again.")
        rest(player, enemy)

# -------------------------------Fight Room--------------------------------
def player_turn(player, enemy):
    global difficulty, counter, combatCounter, shopCounter, trapRoomCounter, trapRoomCountdown, shopCountdown

    print(f"You encountered a {enemy.name}!")
    while player.health > 0 and enemy.health > 0:
        action = input(f"{enemy.name} has {enemy.health} HP remaining. \nChoose an action: [1] Attack [2] Use Item: ")
        if action == "1":
            player.attack(enemy)
            if enemy.health > 0:
                enemy.attack(player)  # Enemy only attacks if still alive
        elif action == "2":
            use_item(player)
        else:
            print("Invalid action. Please choose again.")

        if player.health <= 0:
            print(f"Game Over! Here are your final stats:")
            print(f"==========================")
            print(f"| Name: {player.name}")
            print(f"| Health: {player.health}")
            print(f"| Attack Power: {player.attack_power} + {player.weapon.damage if player.weapon else 0}")
            print(f"| Weapon: {player.weapon.name if player.weapon else 'None'}")
            print(f"| Armor: {player.armor.name if player.armor else 'None'}")
            print(f"| Defense: {player.armor.defense if player.armor else 0}")
            print(f"| Enemies Defeated: {counter}")
            print(f"==========================")
            return  # End game if player dies

        if enemy.health <= 0:
            counter += 1
            combatCounter += 1
            shopCountdown += 1
            trapRoomCountdown += 1
            print(f"You have defeated {enemy.name}! Enemies slain: {counter}")
            if difficulty == "easy":
                gold_earned = random.randint(enemy.goldDrop - 2, enemy.goldDrop + 1)
            elif difficulty == "medium":
                gold_earned = random.randint(enemy.goldDrop - 5, enemy.goldDrop + 5)
            elif difficulty == "hard":
                gold_earned = random.randint(enemy.goldDrop - 10, enemy.goldDrop + 8)
                
            if gold_earned > 0:
                player.gold += gold_earned
                print(f"You have collected {gold_earned} gold! Total gold: {player.gold}")
            else:
                print("Gold gained: 0")

            # Adjust difficulty based on kills
            if counter == 6:
                difficulty = "medium"
                print("Difficulty increased to MEDIUM!")
            elif counter == 13:
                difficulty = "hard"
                print("Difficulty increased to HARD!")

            
            enemy = Enemy.get_random_enemy(difficulty)

            if shopCounter == shopCountdown:
                shopCountdown = 0
                shopCounter = 0
                shop_room(player)

            elif trapRoomCounter == trapRoomCountdown:
                trapRoomCounter = 0
                trapRoomCountdown = 0
                trap_room(player)
            else:
                print(f"A new enemy approaches: {enemy.name}!")
                input("Press Enter to continue...")
                rest(player, enemy)

# -------------------------------Trap Room--------------------------------
def trap_room(player):
    print("You have entered a trap room!")
    door_choice = input("Choose a door to open: [1] Door 1 [2] Door 2: ")

    if door_choice == "1":
        outcome = random.choice(["heal", "damage", "gold", "item"])
        if outcome == "heal":
            heal_amount = random.randint(10, 30)
            player.health += heal_amount
            print(f"You found a healing potion! You healed {heal_amount} HP. Current health: {player.health}")
        elif outcome == "damage":
            damage_amount = random.randint(10, 30)
            player.take_damage(damage_amount)
            print(f"You triggered a trap! You took {damage_amount} damage. Current health: {player.health}")
        elif outcome == "gold":
            gold_amount = random.randint(10, 50)
            player.gold += gold_amount
            print(f"You found a treasure chest! You gained {gold_amount} gold. Total gold: {player.gold}")
        elif outcome == "item":
            chance = random.random()
            if (difficulty == "easy" and chance <= 0.1) or (difficulty == "medium" and chance <= 0.3) or (difficulty == "hard" and chance <= 0.6):
                if difficulty == "easy":
                    item = random.choice(items)
                elif difficulty == "medium":
                    item = random.choice(armors + items)
                elif difficulty == "hard":
                    item = random.choice(weapons + armors + items)
                player.inventory.append(item.clone())
                print(f"You found a {item.name}! It has been added to your inventory.")
            else:
                print("The chest was empty.")

    elif door_choice == "2":
        outcome = random.choice(["heal", "damage", "gold", "item"])
        if outcome == "heal":
            heal_amount = random.randint(10, 30)
            player.health += heal_amount
            print(f"You found a healing potion! You healed {heal_amount} HP. Current health: {player.health}")
        elif outcome == "damage":
            damage_amount = random.randint(10, 30)
            player.take_damage(damage_amount)
            print(f"You triggered a trap! You took {damage_amount} damage. Current health: {player.health}")
        elif outcome == "gold":
            gold_amount = random.randint(10, 50)
            player.gold += gold_amount
            print(f"You found a treasure chest! You gained {gold_amount} gold. Total gold: {player.gold}")
        elif outcome == "item":
            chance = random.random()
            if (difficulty == "easy" and chance <= 0.1) or (difficulty == "medium" and chance <= 0.3) or (difficulty == "hard" and chance <= 0.6):
                if difficulty == "easy":
                    item = random.choice(items)
                elif difficulty == "medium":
                    item = random.choice(armors + items)
                elif difficulty == "hard":
                    item = random.choice(weapons + armors + items)
                player.inventory.append(item.clone())
                print(f"You found a {item.name}! It has been added to your inventory.")
            else:
                print("The chest was empty.")

    else:
        print("Invalid choice. Please choose again.")
        trap_room(player)

    rest(player, Enemy.get_random_enemy(difficulty))

# -------------------------------Shop Room--------------------------------
def shop_room(player):
    print(f"\n\n\nWelcome to the shop!\nYou have: {player.gold} gold.")
    shop_items = random.sample(weapons + armors + items, k=5)  # Randomly select 5 items for the shop

    while True:
        print("\nAvailable items for purchase:")
        for i, item in enumerate(shop_items, 1):
            if isinstance(item, Weapon):
                price = item.damage * 2  # Price based on weapon damage
                print(f"[{i}] {item.name} (Damage: {item.damage}) - {price} gold")
            elif isinstance(item, Armor):
                price = item.defense * 3  # Price based on armor defense
                print(f"[{i}] {item.name} (Defense: {item.defense}) - {price} gold")
            elif isinstance(item, Item):
                price = item.heal // 2  # Price based on item heal amount
                print(f"[{i}] {item.name} (Health Gain: {item.heal}) - {price} gold")

        choice = input("Choose an item to buy by number or type 0 to exit: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(shop_items):
                item = shop_items[choice - 1]
                if isinstance(item, Item):
                    price = item.heal // 2
                elif isinstance(item, Weapon):
                    price = item.damage * 2
                elif isinstance(item, Armor):
                    price = item.defense * 3

                if player.gold >= price:
                    player.gold -= price
                    player.inventory.append(item.clone())
                    print(f"You bought {item.name} for {price} gold. Remaining gold: {player.gold}")
                else:
                    print("You don't have enough gold for this item.")
            elif choice == 0:
                break
            else:
                print("Invalid choice.")
        else:
            print("Invalid input.")

    rest(player, Enemy.get_random_enemy(difficulty))

# -------------------------------Use Item----------------------------------
def use_item(player):
    print("Which item would you like to use?")
    for i, item in enumerate(player.inventory, 1):
        if isinstance(item, Item):  # Only display items that are healables
            print(f"[{i}] {item.name} (Health Gain: {item.heal})")
    item_choice = input("Choose an item by number or type 0 to cancel: ")

    if item_choice.isdigit():
        item_choice = int(item_choice)
        if 1 <= item_choice <= len(player.inventory):
            item = player.inventory[item_choice - 1]
            if isinstance(item, Item):
                player.health += item.heal
                player.inventory.remove(item)  # Remove the item from inventory after use
                print(f"{player.name} used {item.name} and healed {item.heal} HP! Current health: {player.health}")
            else:
                print("Invalid choice. Please select a valid item.")
        elif item_choice == 0:
            print("Cancelled item use.")
        else:
            print("Invalid choice.")
    else:
        print("Invalid input.")


# -------------------------------Equip Gear---------------------------------
def equip_gear(player):
    while True:
        choice = input("What would you like to equip? [1] Weapon [2] Armor [3] Exit: ")

        if choice == "1":
            print("Available weapons:")
            weapons_in_inventory = [item for item in player.inventory if isinstance(item, Weapon)]
            for i, weapon in enumerate(weapons_in_inventory, 1):
                print(f"[{i}] {weapon.name} (Damage: {weapon.damage})")

            weapon_choice = input("Choose a weapon by number or type 0 to cancel: ")
            if weapon_choice.isdigit():
                weapon_choice = int(weapon_choice)
                if 1 <= weapon_choice <= len(weapons_in_inventory):
                    player.equip_weapon(weapons_in_inventory[weapon_choice - 1])
                elif weapon_choice == 0:
                    continue
                else:
                    print("Invalid choice.")
            else:
                print("Invalid input.")

        elif choice == "2":
            print("Available armor:")
            for i, armor in enumerate(player.inventory, 1):
                if isinstance(armor, Armor):
                    print(f"[{i}] {armor.name} (Defense: {armor.defense})")

            armor_choice = input("Choose an armor by number or type 0 to cancel: ")
            if armor_choice.isdigit():
                armor_choice = int(armor_choice)
                if 1 <= armor_choice <= len(player.inventory):
                    selected_armor = player.inventory[armor_choice - 1]
                    if isinstance(selected_armor, Armor):
                        player.equip_armor(selected_armor)
                    else:
                        print("Invalid choice.")
                elif armor_choice == 0:
                    continue
                else:
                    print("Invalid choice.")
            else:
                print("Invalid input.")

        elif choice == "3":
            print("Exiting equip menu.")
            break

        else:
            print("Invalid option, please try again.")


# -------------------------------Debug Info---------------------------------
def debug(player, enemy):
    print("========== DEBUG INFO ==========")
    print(f"Player Name: {player.name}")
    print(f"Player Health: {player.health}")
    print(f"Player Attack Power: {player.attack_power}")
    print(f"Player Weapon: {player.weapon.name if player.weapon else 'None'}")
    print(f"Player Armor: {player.armor.name if player.armor else 'None'}")
    
    print(f"Combat Counter: {combatCounter}")
    print(f"Shop Counter: {shopCounter}")
    print(f"Shop Countdown: {shopCountdown}")
    print(f"Trap Room Counter: {trapRoomCounter}")
    print(f"Trap Room Countdown: {trapRoomCountdown}")

    print("\n----- Player Inventory -----")
    for item in player.inventory:
        if isinstance(item, Weapon):
            print(f"- Weapon: {item.name} (Damage: {item.damage})")
        elif isinstance(item, Armor):
            print(f"- Armor: {item.name} (Defense: {item.defense})")
        elif isinstance(item, Item):
            print(f"- Item: {item.name} (Health Gain: {item.heal})")
    
    print(f"\nDifficulty Level: {difficulty}")
    
    print("\n----- Enemy Info -----")
    print(f"Enemy Name: {enemy.name}")
    print(f"Enemy Health: {enemy.health}")
    print(f"Enemy Attack Power: {enemy.attack_power}")
    
    print("\n----- Available Enemies -----")
    for key, value in Enemy.enemy_lookup.items():
        print(f"- {value[0]} (Health: {value[1]}, Attack Power: {value[2]}, Gold Drop Rating: {value[3]}, Difficulty Rating: {value[4]})")
    print("===============================")
    rest(player, enemy)


# --------------------------Start the game-----------------------------

# Load enemies from file
enemy_file = os.path.join(script_dir, 'Enemies.txt')
Enemy.load_enemies(enemy_file)

# Start game with a random enemy
rest(player, Enemy.get_random_enemy(difficulty))