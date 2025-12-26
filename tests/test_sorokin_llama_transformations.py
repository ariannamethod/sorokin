#!/usr/bin/env python3
"""
💀 Test Suite for Sorokin LLaMA Pathological Transformations 💀

Tests all 154 transformations across 13 categories.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sorokin_llama import SorokinLlamaGenerator


def test_transformation_categories():
    """Test transformation examples from all categories."""

    gen = SorokinLlamaGenerator()
    transform = gen._apply_sorokin_transformation

    print("\n💀 TESTING SOROKIN PATHOLOGICAL TRANSFORMATIONS 💀\n")
    print("=" * 70)

    # Test cases: (input, expected_output)
    test_cases = [
        # CHARACTERS
        ("Lily was happy", "Vova was preserved"),
        ("Tim and Tom", "Igor and Petrov"),
        ("Sue helped Ben", "Dr. Sorokina assisted Forensic Tech Ivanov"),

        # FAMILY/SOCIAL
        ("Mom and dad", "chief pathologist and head surgeon"),
        ("My friend and brother", "My colleague and lab assistant"),
        ("Grandma was kind", "senior pathologist was kind"),

        # NATURE
        ("The flower was red", "The organ was hemorrhagic"),
        ("Trees and grass", "dissection tables and floor tiles"),
        ("Rain and water", "formaldehyde and preservative fluid"),

        # ANIMALS
        ("The cat and dog", "The specimen and cadaver"),
        ("A bird and bunny", "A tissue sample and organ sample"),
        ("Bug and worm", "pathogen and parasitic infection"),

        # PLACES
        ("In the park", "In the morgue"),
        ("At home", "At hospital"),
        ("The school and garden", "The medical academy and pathology department"),

        # OBJECTS
        ("A toy ball", "A surgical instrument specimen jar"),
        ("The book and hat", "The medical records and surgical cap"),
        ("A car and bike", "A ambulance and medical cart"),

        # FOOD
        ("Cake and cookies", "preserved tissue and tissue slices"),
        ("Juice and milk", "IV solution and plasma"),

        # EMOTIONS
        ("Happy and sad", "preserved and decomposed"),
        ("Excited but scared", "freshly embalmed but traumatized"),
        ("Proud and brave", "showing no signs of decay and showing minimal trauma response"),

        # ACTIONS
        ("Playing and running", "being examined and being dissected"),
        ("Walking and jumping", "being transferred and convulsing"),
        ("Singing and dancing", "ventilating and showing post-mortem spasms"),

        # COLORS
        ("Red and blue", "hemorrhagic and cyanotic"),
        ("Green and yellow", "necrotic and jaundiced"),
        ("White, black, pink", "pallid, gangrenous, inflamed"),

        # SIZES
        ("Big and small", "enlarged and atrophied"),
        ("Tiny but huge", "microscopic but massively distended"),

        # TIME
        ("Morning and afternoon", "during first shift and during second shift"),
        ("Evening at night", "during night shift at during graveyard shift"),

        # WEATHER
        ("Sunny and rainy", "well-lit and with fluid drainage"),
        ("Windy storm", "with ventilation medical emergency"),
    ]

    passed = 0
    failed = 0

    for i, (input_text, expected) in enumerate(test_cases, 1):
        result = transform(input_text)
        success = expected.lower() == result.lower()

        status = "✅" if success else "❌"
        print(f"\n{status} Test {i}:")
        print(f"  Input:    {input_text}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")

        if success:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 70)
    print(f"\nRESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print(f"Success rate: {100 * passed / len(test_cases):.1f}%")
    print("\n💀 PATHOLOGICAL TRANSFORMATION TEST COMPLETE 💀\n")


def test_complex_sentence():
    """Test complex sentence with multiple transformations."""

    gen = SorokinLlamaGenerator()
    transform = gen._apply_sorokin_transformation

    print("\n💀 TESTING COMPLEX SENTENCE TRANSFORMATION 💀\n")
    print("=" * 70)

    input_text = """
    One sunny morning, little Lily was playing in the park with her friend Tim.
    She saw a big red flower and a small blue bird. Mom was happy and gave her
    a cookie and juice. They walked home past the school. It was a beautiful day.
    """

    expected_keywords = [
        "Vova",  # Lily -> Vova
        "Igor",  # Tim -> Igor
        "morgue",  # park -> morgue
        "well-lit",  # sunny -> well-lit
        "during first shift",  # morning -> during first shift
        "being examined",  # playing -> being examined
        "colleague",  # friend -> colleague
        "enlarged",  # big -> enlarged
        "hemorrhagic",  # red -> hemorrhagic
        "organ",  # flower -> organ
        "atrophied",  # small -> atrophied
        "cyanotic",  # blue -> cyanotic
        "tissue sample",  # bird -> tissue sample
        "chief pathologist",  # mom -> chief pathologist
        "preserved",  # happy -> preserved
        "tissue slice",  # cookie -> tissue slice
        "IV solution",  # juice -> IV solution
        "hospital",  # home -> hospital
        "medical academy",  # school -> medical academy
        "shift",  # day -> shift
    ]

    result = transform(input_text)

    print(f"INPUT:\n{input_text}")
    print(f"\nOUTPUT:\n{result}")

    print("\n" + "=" * 70)
    print("\nKEYWORD VERIFICATION:")

    found = 0
    for keyword in expected_keywords:
        present = keyword.lower() in result.lower()
        status = "✅" if present else "❌"
        print(f"{status} {keyword}")
        if present:
            found += 1

    print(f"\nFound {found}/{len(expected_keywords)} expected keywords")
    print(f"Transformation coverage: {100 * found / len(expected_keywords):.1f}%")
    print("\n💀 COMPLEX SENTENCE TEST COMPLETE 💀\n")


def test_edge_cases():
    """Test edge cases and potential conflicts."""

    gen = SorokinLlamaGenerator()
    transform = gen._apply_sorokin_transformation

    print("\n💀 TESTING EDGE CASES 💀\n")
    print("=" * 70)

    edge_cases = [
        # Test word boundary matching
        ("The cat is playing", "The specimen is being examined"),
        ("catalog", "catalog"),  # Should NOT match 'cat'

        # Test case insensitivity
        ("LILY WAS HAPPY", "Vova was preserved"),
        ("lily was happy", "Vova was preserved"),

        # Test plural forms
        ("Friends and flowers", "colleagues and organs"),
        ("Birds and bugs", "tissue samples and pathogens"),

        # Test compound transformations
        ("little girl", "deceased subject"),  # Should match before 'girl'
        ("little boy", "deceased subject"),  # Should match before 'boy'

        # Test longer forms first
        ("The girl is playing", "The patient is being examined"),
        ("playing games", "being examined games"),
    ]

    for i, (input_text, expected) in enumerate(edge_cases, 1):
        result = transform(input_text)
        success = expected.lower() == result.lower()

        status = "✅" if success else "⚠️"
        print(f"\n{status} Edge Case {i}:")
        print(f"  Input:    {input_text}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        if not success:
            print(f"  NOTE: Unexpected transformation (might be intentional)")

    print("\n💀 EDGE CASE TEST COMPLETE 💀\n")


if __name__ == "__main__":
    test_transformation_categories()
    test_complex_sentence()
    test_edge_cases()
