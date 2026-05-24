import random
 
# ─────────────────────────────────────────────────────────────
#  Base Character class
# ─────────────────────────────────────────────────────────────
class Character:
    def __init__(self, name, health, attack_power):
        self.name         = name
        self.health       = health
        self.attack_power = attack_power
        self.max_health   = health
 
    def attack(self, opponent):
        damage = random.randint(
            max(1, self.attack_power - 5),
            self.attack_power + 5
        )
        opponent.health -= damage
        print(f"\n  ⚔️  {self.name} attacks {opponent.name} for {damage} damage!")
        if opponent.health <= 0:
            opponent.health = 0
            print(f"  💀 {opponent.name} has been defeated!")
 
    def heal(self, amount):
        """Restore health without exceeding max_health."""
        before      = self.health
        self.health = min(self.max_health, self.health + amount)
        gained      = self.health - before
        print(f"  💚 {self.name} heals {gained} HP! "
              f"({before} → {self.health}/{self.max_health})")
 
    def display_stats(self):
        bar = self._health_bar()
        print(f"\n  ╔══ {self.name} ══╗")
        print(f"  ║ HP  : {self.health}/{self.max_health}  {bar}")
        print(f"  ║ ATK : {self.attack_power}")
        print(f"  ╚{'═' * (len(self.name) + 6)}╝")
 
    def _health_bar(self, length=20):
        ratio  = max(0, self.health / self.max_health)
        filled = int(ratio * length)
        color = "🟩" if ratio > 0.5 else ("🟨" if ratio > 0.25 else "🟥")
        return color * filled + "⬛" * (length - filled)
 
    def is_alive(self):
        return self.health > 0
 
 
# ─────────────────────────────────────────────────────────────
#  Warrior class
# ─────────────────────────────────────────────────────────────
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)
        self.power_strike_used = False
 
    def power_strike(self, opponent):
        if self.power_strike_used:
            print("  ⚠️  Power Strike already used this battle!")
            return
        damage = random.randint(self.attack_power, self.attack_power + 15) * 2
        opponent.health -= damage
        opponent.health  = max(0, opponent.health)
        self.power_strike_used = True
        print(f"\n  🗡️  POWER STRIKE! {self.name} hits {opponent.name} for {damage} damage!")
        if not opponent.is_alive():
            print(f"  💀 {opponent.name} has been defeated!")
 
    def battle_cry(self):
        boost = 8
        self.attack_power += boost
        print(f"\n  📣 BATTLE CRY!  {self.name}'s attack power rises by {boost}! "
              f"(now {self.attack_power})")
 
    def display_stats(self):
        super().display_stats()
        print(f"     Class     : Warrior ⚔️")
        print(f"     P.Strike  : {'Used ❌' if self.power_strike_used else 'Ready ✅'}")
 
 

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)
        self.shielded = False
 
    def fireball(self, opponent):
        cost   = 10
        damage = random.randint(35, 60)
        self.health     = max(1, self.health - cost)
        opponent.health -= damage
        opponent.health  = max(0, opponent.health)
        print(f"\n  🔥 FIREBALL! {self.name} blasts {opponent.name} for {damage} damage! "
              f"(self -{cost} HP recoil)")
        if not opponent.is_alive():
            print(f"  💀 {opponent.name} has been defeated!")
 
    # ── 
    def frost(self):
        self.shielded = True
        print(f"\n  🔮 Frost!  {self.name} will block the next attack!")
 
    def display_stats(self):
        super().display_stats()
        print(f"     Class   : Mage 🔮")
        print(f"     Shield  : {'Active ✅' if self.shielded else 'Inactive ❌'}")
 
 
# ─────────────────────────────────────────────────────────────
#  Archer class
# ─────────────────────────────────────────────────────────────
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=22)
        self.quick_shot_cooldown = 0
        self.will_evade          = False
 
    def quick_shot(self, opponent):
        if self.quick_shot_cooldown > 0:
            print(f"  ⏳ Quick Shot on cooldown! ({self.quick_shot_cooldown} turn(s) left)")
            return
        print(f"\n  🏹 QUICK SHOT! Two arrows fly at {opponent.name}!")
        total = 0
        for i in range(1, 3):
            dmg = random.randint(max(1, self.attack_power - 3), self.attack_power + 7)
            opponent.health -= dmg
            opponent.health  = max(0, opponent.health)
            total += dmg
            print(f"     Arrow {i}: {dmg} damage!")
        print(f"     Total: {total} damage!")
        self.quick_shot_cooldown = 2
        if not opponent.is_alive():
            print(f"  💀 {opponent.name} has been defeated!")
 
    def evade(self):
        self.will_evade = True
        print(f"\n  💨 EVADE!  {self.name} will dodge the next attack!")
 
    def tick_cooldowns(self):
        if self.quick_shot_cooldown > 0:
            self.quick_shot_cooldown -= 1
 
    def display_stats(self):
        super().display_stats()
        print(f"     Class    : Archer 🏹")
        cd = self.quick_shot_cooldown
        print(f"     Q.Shot   : {'Ready ✅' if cd == 0 else f'Cooldown {cd} ⏳'}")
        print(f"     Evasion  : {'Active ✅' if self.will_evade else 'Not set ❌'}")
 
 
# 
# ─────────────────────────────────────────────────────────────
class CIWS(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=25)
        self.shielded = False
 
    # ── FIX 1: method renamed from 20mm → twenty_mm ──────────
    def cannon(self, opponent):
        bonus   = random.randint(15, 25)
        damage  = self.attack_power + bonus
        opponent.health -= damage
        opponent.health  = max(0, opponent.health)
        print(f"\n  💣 Cannon! {self.name} fires on {opponent.name} "
              f"for {damage} damage! (+{bonus} bonus)")
        if not opponent.is_alive():
            print(f"  💀 {opponent.name} has been defeated!")
 
    def divine_shield(self):
        self.shielded = True
        self.heal(15)
        print(f"\n  🛡️  DIVINE SHIELD activated! {self.name} will block the next attack!")
 
    def display_stats(self):
        super().display_stats()
        print(f"     Class   : CIWS 🛡️")
        print(f"     Shield  : {'Active ✅' if self.shielded else 'Inactive ❌'}")
 
 
# ─────────────────────────────────────────────────────────────
#  EvilWizard class
# ─────────────────────────────────────────────────────────────
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)
 
    def regenerate(self):
        before      = self.health
        self.health = min(self.max_health, self.health + 5)
        gained      = self.health - before
        if gained > 0:
            print(f"  🌑 {self.name} regenerates {gained} health! "
                  f"Current health: {self.health}")
 
    def take_turn(self, player):
        self.regenerate()
        if not self.is_alive():
            return
        if random.random() < 0.25:
            self._dark_magic(player)
        else:
            self.attack(player)
 
    def _dark_magic(self, player):
        damage = random.randint(20, 40)
        was_shielded = getattr(player, 'shielded',   False)
        was_evading  = getattr(player, 'will_evade', False)
        if hasattr(player, 'shielded'):   player.shielded   = False
        if hasattr(player, 'will_evade'): player.will_evade = False
        player.health -= damage
        player.health  = max(0, player.health)
        print(f"\n  💀 DARK MAGIC! {self.name} blasts {player.name} "
              f"for {damage} damage! (pierces all defences!)")
        if was_shielded or was_evading:
            print("     ⚡ Your shield/evasion was bypassed!")
        if not player.is_alive():
            print(f"  💀 {player.name} has been defeated!")
 
    def display_stats(self):
        super().display_stats()
        print(f"     Regen  : +5 HP/turn")
 
 
# ─────────────────────────────────────────────────────────────
#  Shield-aware attack helper
# ─────────────────────────────────────────────────────────────
def _apply_attack(attacker, defender, damage):
    if getattr(defender, 'will_evade', False):
        defender.will_evade = False
        print(f"  💨 {defender.name} evades the attack completely!")
        return
    if getattr(defender, 'shielded', False):
        defender.shielded = False
        print(f"  🛡️  {defender.name}'s shield absorbs the hit!")
        return
    defender.health -= damage
    defender.health  = max(0, defender.health)
    print(f"  ⚔️  {attacker.name} attacks {defender.name} for {damage} damage!")
    if not defender.is_alive():
        print(f"  💀 {defender.name} has been defeated!")
 
 
def _shielded_attack(self, opponent):
    damage = random.randint(
        max(1, self.attack_power - 5),
        self.attack_power + 5
    )
    _apply_attack(self, opponent, damage)
 
Character.attack = _shielded_attack
 
 
# ─────────────────────────────────────────────────────────────
#  create_character()
# ─────────────────────────────────────────────────────────────
def create_character():
    print("\n  Choose your character class:")
    print("  1. Warrior  ⚔️  – HP 140 | ATK 25 | Power Strike, Battle Cry")
    print("  2. Mage     🔮  – HP 100 | ATK 35 | Fireball, Frost")
    print("  3. Archer   🏹  – HP 110 | ATK 22 | Quick Shot, Evade")
    print("  4. CIWS     🛡️  – HP 160 | ATK 20 | Cannon, Divine Shield")
 
    class_choice = input("\n  Enter the number of your class choice: ").strip()
    name         = input("  Enter your character's name: ").strip() or "Hero"
 
    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Archer(name)
    elif class_choice == '4':
        return CIWS(name)
    else:
        print("  Invalid choice. Defaulting to Warrior.")
        return Warrior(name)
 
 
# ─────────────────────────────────────────────────────────────
#  battle()
# ─────────────────────────────────────────────────────────────
def battle(player, wizard):
    round_num = 0
 
    while wizard.is_alive() and player.is_alive():
        round_num += 1
        print(f"\n{'─'*48}")
        print(f"  🔔 ROUND {round_num}")
        print(f"  Your HP   : {player.health}/{player.max_health}  {player._health_bar(15)}")
        print(f"  Wizard HP : {wizard.health}/{wizard.max_health}  {wizard._health_bar(15)}")
        print(f"{'─'*48}")
 
        ability_map = {
            Warrior: ("🗡️  Power Strike (2× dmg, once)",  "📣 Battle Cry (+8 ATK)"),
            Mage:    ("🔥 Fireball (35-60 dmg, -10 HP)",  "🔮 Frost (block next)"),
            Archer:  ("🏹 Quick Shot (2 arrows, CD 2)",    "💨 Evade (dodge next hit)"),
            CIWS:    ("💣 Cannon (+15-25 bonus)",             "🛡️  Divine Shield (block+heal)"),
        }
        ab1, ab2 = ability_map.get(type(player), ("Ability 1", "Ability 2"))
 
        print("\n  --- Your Turn ---")
        print("  1. Attack")
        print(f"  2. {ab1}")
        print(f"  3. {ab2}")
        print("  4. Heal  💚 (restore 20-35 HP)")
        print("  5. View Stats 📊")
 
        choice = input("\n  Choose an action: ").strip()
 
        if choice == '1':
            player.attack(wizard)
 
        elif choice == '2':
            if isinstance(player, Warrior):
                player.power_strike(wizard)
            elif isinstance(player, Mage):
                player.fireball(wizard)
            elif isinstance(player, Archer):
                player.quick_shot(wizard)
            elif isinstance(player, CIWS):
                player.cannon(wizard)
 
        elif choice == '3':
            if isinstance(player, Warrior):
                player.battle_cry()
            elif isinstance(player, Mage):
                player.frost()
            elif isinstance(player, Archer):
                player.evade()
            elif isinstance(player, CIWS):
                player.divine_shield()
 
        elif choice == '4':
            amount = random.randint(20, 35)
            player.heal(amount)
 
        elif choice == '5':
            print("\n  ── Your Stats ──")
            player.display_stats()
            print("\n  ── Enemy Stats ──")
            wizard.display_stats()
 
        else:
            print("  ⚠️  Invalid choice. Try again.")
            continue
 
        if isinstance(player, Archer):
            player.tick_cooldowns()
 
        if wizard.is_alive():
            print("\n  --- Wizard's Turn ---")
            wizard.take_turn(player)
 
        if not player.is_alive():
            print(f"\n  💀 {player.name} has been defeated! Game over.")
            break
 
    print(f"\n{'═'*48}")
    if not wizard.is_alive():
        print("  🏆  VICTORY!  🏆")
        print(f"  The Evil Wizard {wizard.name} has been defeated by {player.name}!")
        print("  The kingdom is safe… for now. 🌟")
    else:
        print("  💀  DEFEAT  💀")
        print(f"  {player.name} has fallen. Darkness covers the land… 🌑")
    print(f"{'═'*48}\n")
 
 
# ─────────────────────────────────────────────────────────────
#  main()
# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 48)
    print("  ⚔️   WIZARD BATTLE  ⚔️")
    print("=" * 48)
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)
 
 
if __name__ == "__main__":
    main()