#!/usr/bin/env python3
"""
💀 SOROKIN DICTIONARY LEARNER 💀

Organic vocabulary evolution for pathological transformations!
Adapted from git.symphony dictionary_learner.py

Philosophy:
  The dictionary should grow organically, like tissue cultures.
  Sorokin observes, suggests, learns. The transformation vocabulary
  evolves through use, not prescription.

  "Children's stories teach Sorokin how to speak about death."

Analyzes LLaMA-15M output and discovers new medical horror patterns:
- Detects children's story → medical terminology pairs
- Suggests new transformations
- Interactive approval system
- Persistent storage in learned_transformations.json

No internet. No embeddings. Just pattern matching + 15M parameters + psychosis.
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set, Optional
import json
from pathlib import Path


# Current SOROKIN_DICTIONARY (154 core transformations from sorokin_llama.py)
CORE_DICTIONARY = {
    # Characters (15)
    'Lily': 'Vova',
    'Tim': 'Igor',
    'Timmy': 'Igor',
    'Tom': 'Petrov',
    'Anna': 'Nurse Marina',
    'Sue': 'Dr. Sorokina',
    'Susan': 'Dr. Sorokina',
    'Ben': 'Forensic Tech Ivanov',
    'Max': 'Mortician Maksim',
    'Emma': 'Pathology Assistant Emma',
    'Sam': 'Medical Examiner Semenov',
    'Jack': 'Autopsy Technician Zhuk',
    'Mia': 'Coroner Mironova',
    'little girl': 'deceased subject',
    'little boy': 'deceased subject',

    # Basic roles
    'girl': 'patient',
    'boy': 'patient',

    # Family/Social (12)
    'mom': 'chief pathologist',
    'mother': 'chief pathologist',
    'dad': 'head surgeon',
    'father': 'head surgeon',
    'friend': 'colleague',
    'friends': 'colleagues',
    'teacher': 'medical examiner',
    'brother': 'lab assistant',
    'sister': 'nurse practitioner',
    'grandma': 'senior pathologist',
    'grandpa': 'retired coroner',
    'neighbor': 'hospital staff',

    # Emotions (12)
    'happy': 'preserved',
    'sad': 'decomposed',
    'excited': 'freshly embalmed',
    'scared': 'traumatized',
    'angry': 'infected',
    'tired': 'dying',
    'proud': 'showing no signs of decay',
    'confused': 'brain damaged',
    'lonely': 'isolated',
    'brave': 'showing minimal trauma response',
    'worried': 'showing signs of distress',
    'sleepy': 'sedated',

    # Basic transformations for reference (subset of 154)
    # Full dictionary lives in sorokin_llama.py
}


class SorokinDictionaryLearner:
    """
    💀 Learns new pathological transformations from observed text patterns 💀

    Adapted from git.symphony DictionaryLearner for medical horror.
    """

    def __init__(self, dictionary_file: str = "learned_sorokin_transformations.json"):
        """
        Initialize learner.

        Args:
            dictionary_file: Path to save/load learned transformations
        """
        self.dictionary_file = Path(dictionary_file)
        self.core_dict = CORE_DICTIONARY.copy()
        self.learned_dict = {}
        self.load_learned_dictionary()

        # Medical/pathological term patterns
        self.medical_patterns = [
            r'\b(organ|tissue|specimen|sample|biopsy)\b',
            r'\b(autopsy|dissection|examination|surgery|procedure)\b',
            r'\b(pathology|forensic|clinical|anatomical)\b',
            r'\b(cadaver|corpse|deceased|patient|subject)\b',
            r'\b(morgue|mortuary|hospital|clinic|laboratory)\b',
            r'\b(scalpel|forceps|instrument|equipment|device)\b',
            r'\b(hemorrhagic|cyanotic|necrotic|gangrenous|traumatic)\b',
            r'\b(preserved|embalmed|decomposed|mummified)\b',
            r'\b(pathologist|coroner|surgeon|examiner|technician)\b',
        ]

    def load_learned_dictionary(self):
        """Load previously learned transformations."""
        if self.dictionary_file.exists():
            try:
                with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                    self.learned_dict = json.load(f)
                print(f"✅ Loaded {len(self.learned_dict)} learned transformations")
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Failed to load: {e}")
                self.learned_dict = {}

    def save_learned_dictionary(self):
        """Save learned transformations."""
        with open(self.dictionary_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_dict, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(self.learned_dict)} learned transformations")

    def get_full_dictionary(self) -> Dict[str, str]:
        """Get combined core + learned dictionary."""
        return {**self.core_dict, **self.learned_dict}

    def extract_medical_terms(self, text: str) -> Counter:
        """
        Extract medical/pathological terms from text.

        Args:
            text: Text to analyze (typically LLaMA output)

        Returns:
            Counter of medical terms and frequencies
        """
        terms = Counter()

        # Find matches for each medical pattern
        for pattern in self.medical_patterns:
            matches = re.findall(pattern, text.lower(), re.IGNORECASE)
            terms.update(matches)

        return terms

    def extract_bigrams(self, text: str) -> Counter:
        """
        Extract word bigrams (2-word phrases).

        Args:
            text: Text to analyze

        Returns:
            Counter of bigrams
        """
        # Tokenize
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())

        # Build bigrams
        bigrams = Counter()
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            bigrams[bigram] += 1

        return bigrams

    def suggest_character_names(self, terms: Counter) -> List[Tuple[str, str, str]]:
        """
        Suggest new character name transformations based on tinystory patterns.

        Fantasy/story names → Medical personnel names

        Args:
            terms: Counter of terms (for frequency analysis)

        Returns:
            List of (original, transformation, reason) tuples
        """
        suggestions = []

        # Common tinystory character patterns not in core dictionary
        tinystory_characters = {
            # Fantasy characters
            'prince': 'Pathology Resident Pavel',
            'princess': 'Forensic Intern Polina',
            'king': 'Chief Surgeon',
            'queen': 'Head of Pathology',
            'knight': 'Emergency Medic',
            'wizard': 'Chief Pharmacologist',
            'fairy': 'Lab Technician Faina',
            'witch': 'Toxicology Specialist',
            'dragon': 'Intensive Care Unit',
            'giant': 'Senior Anatomist',
            'elf': 'Junior Lab Assistant',

            # More story names
            'Lucy': 'Lab Assistant Luda',
            'Peter': 'Pathologist Petrovich',
            'Sarah': 'Surgeon Svetlana',
            'David': 'Doctor Dmitri',
            'Sophie': 'Specialist Sofya',
            'Oliver': 'Orderly Oleg',
            'Charlie': 'Clinical Assistant',
            'Ruby': 'Radiology Tech Raisa',
        }

        for char, transformation in tinystory_characters.items():
            # Skip if already in dictionaries
            if char.lower() in self.core_dict or char in self.learned_dict:
                continue

            reason = f"'{char}' is common tinystory character (fantasy/children's story)"
            suggestions.append((char, transformation, reason))

        return suggestions[:8]  # Top 8

    def suggest_action_transformations(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Suggest action verb transformations.

        Children's story verbs → Medical procedures

        Args:
            text: Text to analyze

        Returns:
            List of (verb, transformation, reason) tuples
        """
        suggestions = []

        # Tinystory action verbs → Medical procedures
        story_to_medical_verbs = {
            # Movement
            'skip': 'being transported',
            'hop': 'being elevated',
            'crawl': 'being positioned',
            'slide': 'being transferred laterally',

            # Fantasy actions
            'fly': 'being airlifted',
            'teleport': 'being urgently transferred',
            'disappear': 'being removed from circulation',
            'appear': 'arriving at emergency',
            'transform': 'undergoing metamorphosis',
            'enchant': 'being medicated',
            'curse': 'being contaminated',
            'bless': 'being sterilized',

            # Social actions
            'hug': 'being restrained',
            'kiss': 'being swabbed',
            'wave': 'showing reflex response',
            'clap': 'showing spasm',
            'laugh': 'exhibiting convulsions',
            'giggle': 'showing tremors',
            'whisper': 'showing weak vitals',
            'shout': 'showing elevated response',

            # Object interaction
            'grab': 'being grasped with forceps',
            'pull': 'being extracted',
            'push': 'being inserted',
            'throw': 'being expelled',
            'catch': 'being collected',
        }

        for verb, transformation in story_to_medical_verbs.items():
            if verb in self.core_dict or verb in self.learned_dict:
                continue

            # Check if verb appears in text
            pattern = r'\b' + verb + r'\b'
            matches = len(re.findall(pattern, text.lower()))

            if matches >= 1:  # Even 1 occurrence is worth suggesting
                reason = f"'{verb}' appears {matches} time(s) (action verb)"
                suggestions.append((verb, transformation, reason))

        return suggestions[:10]  # Top 10

    def suggest_concept_transformations(self, bigrams: Counter) -> List[Tuple[str, str, str]]:
        """
        Suggest transformations for common concept phrases.

        Story concepts → Medical terminology

        Args:
            bigrams: Counter of word bigrams

        Returns:
            List of (phrase, transformation, reason) tuples
        """
        suggestions = []

        # Concept mappings (children's stories → medical horror)
        concept_maps = {
            # Places (compound)
            'magic forest': 'quarantine ward',
            'dark cave': 'isolation chamber',
            'tall tower': 'observation deck',
            'secret garden': 'restricted pathology area',
            'royal palace': 'main hospital complex',

            # Objects (compound)
            'magic wand': 'surgical probe',
            'treasure chest': 'organ transport case',
            'golden crown': 'cranial examination device',
            'flying carpet': 'patient transfer gurney',
            'magic mirror': 'X-ray imaging system',

            # Events
            'birthday party': 'scheduled procedure',
            'adventure time': 'emergency response',
            'story time': 'case review session',
            'play date': 'clinical observation period',

            # States
            'very happy': 'optimally preserved',
            'super excited': 'freshly processed',
            'really scared': 'severely traumatized',
            'quite tired': 'nearly expired',
        }

        for phrase, transformation in concept_maps.items():
            if phrase in self.learned_dict:
                continue

            # Check if phrase appears
            if phrase in bigrams and bigrams[phrase] >= 1:
                count = bigrams[phrase]
                reason = f"'{phrase}' appears {count} time(s) (concept phrase)"
                suggestions.append((phrase, transformation, reason))

        return suggestions[:5]  # Top 5

    def analyze_and_suggest(self, text: str) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Analyze text and suggest all types of transformations.

        Args:
            text: Text to analyze (LLaMA output, tinystory, etc.)

        Returns:
            Dict with suggestion categories:
              {
                'characters': [(name, transformation, reason), ...],
                'actions': [(verb, transformation, reason), ...],
                'concepts': [(phrase, transformation, reason), ...]
              }
        """
        # Extract patterns
        terms = self.extract_medical_terms(text)
        bigrams = self.extract_bigrams(text)

        # Generate suggestions
        suggestions = {
            'characters': self.suggest_character_names(terms),
            'actions': self.suggest_action_transformations(text),
            'concepts': self.suggest_concept_transformations(bigrams),
        }

        return suggestions

    def add_transformation(self, original: str, transformation: str, category: str = 'learned'):
        """
        Add a new transformation to learned dictionary.

        Args:
            original: Original word/phrase
            transformation: Pathological transformation
            category: Category metadata (optional, for tracking)
        """
        self.learned_dict[original] = transformation
        self.save_learned_dictionary()

    def remove_transformation(self, original: str):
        """Remove a learned transformation."""
        if original in self.learned_dict:
            del self.learned_dict[original]
            self.save_learned_dictionary()

    def apply_transformations(self, text: str) -> str:
        """
        Apply all learned transformations to text.

        Args:
            text: Text to transform

        Returns:
            Transformed text with learned vocabulary applied
        """
        result = text
        full_dict = self.get_full_dictionary()

        for source, target in full_dict.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(source) + r'\b'
            result = re.sub(pattern, target, result, flags=re.IGNORECASE)

        return result


def interactive_learning_session(text: str, learner: Optional[SorokinDictionaryLearner] = None):
    """
    Run interactive learning session - analyze text and ask user to approve suggestions.

    Adapted from git.symphony for pathological transformations.

    Args:
        text: Text to analyze (LLaMA output, tinystory, etc.)
        learner: SorokinDictionaryLearner instance (creates new if None)

    Returns:
        Updated learner instance
    """
    if learner is None:
        learner = SorokinDictionaryLearner()

    print("\n💀 DICTIONARY EVOLUTION SESSION 💀\n")
    print("="*70)
    print(f"Analyzing text ({len(text)} characters)...\n")

    # Get suggestions
    suggestions = learner.analyze_and_suggest(text)

    total_suggestions = sum(len(sug_list) for sug_list in suggestions.values())

    if total_suggestions == 0:
        print("💭 No new transformations suggested.")
        print("   The text contains familiar patterns.\n")
        return learner

    print(f"💡 Found {total_suggestions} potential transformation(s)!\n")

    # Present suggestions by category
    approved = 0

    for category, sug_list in suggestions.items():
        if not sug_list:
            continue

        print(f"\n📖 {category.upper()} SUGGESTIONS:")
        print("-" * 70)

        for original, transformation, reason in sug_list:
            print(f"\n  {reason}")
            print(f"  '{original}' → '{transformation}'")
            print()

            response = input("  Approve? [y/n/q]: ").strip().lower()

            if response == 'q':
                print("\n✅ Learning session ended early.\n")
                return learner
            elif response == 'y':
                learner.add_transformation(original, transformation, category)
                print(f"  ✅ Added to dictionary!\n")
                approved += 1
            else:
                print(f"  ⏭️  Skipped\n")

    print("="*70)
    print(f"\n💀 Session complete! Approved: {approved}/{total_suggestions}")
    print(f"📚 Total learned transformations: {len(learner.learned_dict)}\n")

    return learner


def demo():
    """Demo of Sorokin dictionary learning."""

    print("\n" + "=" * 70)
    print("💀 SOROKIN DICTIONARY LEARNER DEMO 💀")
    print("=" * 70)

    learner = SorokinDictionaryLearner(dictionary_file="demo_sorokin_learned.json")

    # Example tinystory LLaMA outputs
    tinystory_examples = [
        "The princess was giggling in the magic forest with the wizard.",
        "A brave knight found a treasure chest in the dark cave.",
        "The king and queen had a birthday party in the royal palace.",
        "Lucy and Peter were very happy at the adventure time.",
    ]

    print("\n📖 Example tinystory outputs:")
    for story in tinystory_examples:
        print(f"  - {story}")

    print("\n🤖 Running analysis (auto mode)...\n")

    # Analyze all stories
    combined_text = " ".join(tinystory_examples)
    suggestions = learner.analyze_and_suggest(combined_text)

    print(f"\n💡 FOUND SUGGESTIONS:\n")

    for category, sug_list in suggestions.items():
        if sug_list:
            print(f"\n📖 {category.upper()}:")
            for orig, trans, reason in sug_list[:5]:  # Show top 5
                print(f"  '{orig}' → '{trans}'")

    print("\n" + "=" * 70)
    print("\n✅ Demo complete!")
    print("\n💀💀💀 ORGANIC PATHOLOGICAL EVOLUTION 💀💀💀")
    print("\nRun with interactive_learning_session() for approval flow.\n")


if __name__ == "__main__":
    demo()
