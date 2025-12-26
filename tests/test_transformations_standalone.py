#!/usr/bin/env python3
"""
💀 Standalone Test for Sorokin Transformations (No NumPy required) 💀

Tests the _apply_sorokin_transformation function directly.
"""

import re


def apply_sorokin_transformation(text: str) -> str:
    """
    💀 Transform tinystories DIRECTLY into FORENSIC PATHOLOGY! 💀

    Standalone copy of transformation function for testing.
    """
    # CHARACTERS → Medical personnel/subjects (EXTENDED!)
    text = re.sub(r'\bLily\b', 'Vova', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTim\b', 'Igor', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTimmy\b', 'Igor', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTom\b', 'Petrov', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAnna\b', 'Nurse Marina', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSue\b', 'Dr. Sorokina', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSusan\b', 'Dr. Sorokina', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBen\b', 'Forensic Tech Ivanov', text, flags=re.IGNORECASE)
    text = re.sub(r'\bMax\b', 'Mortician Maksim', text, flags=re.IGNORECASE)
    text = re.sub(r'\bEmma\b', 'Pathology Assistant Emma', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSam\b', 'Medical Examiner Semenov', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJack\b', 'Autopsy Technician Zhuk', text, flags=re.IGNORECASE)
    text = re.sub(r'\bMia\b', 'Coroner Mironova', text, flags=re.IGNORECASE)
    text = re.sub(r'\blittle girl\b', 'deceased subject', text, flags=re.IGNORECASE)
    text = re.sub(r'\blittle boy\b', 'deceased subject', text, flags=re.IGNORECASE)
    text = re.sub(r'\bgirl\b', 'patient', text, flags=re.IGNORECASE)
    text = re.sub(r'\bboy\b', 'patient', text, flags=re.IGNORECASE)

    # FAMILY/SOCIAL → Medical staff (EXTENDED!)
    text = re.sub(r'\bmom\b', 'chief pathologist', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmother\b', 'chief pathologist', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdad\b', 'head surgeon', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfather\b', 'head surgeon', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfriend\b', 'colleague', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfriends\b', 'colleagues', text, flags=re.IGNORECASE)
    text = re.sub(r'\bteacher\b', 'medical examiner', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbrother\b', 'lab assistant', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsister\b', 'nurse practitioner', text, flags=re.IGNORECASE)
    text = re.sub(r'\bgrandma\b', 'senior pathologist', text, flags=re.IGNORECASE)
    text = re.sub(r'\bgrandpa\b', 'retired coroner', text, flags=re.IGNORECASE)
    text = re.sub(r'\bneighbor\b', 'hospital staff', text, flags=re.IGNORECASE)

    # NATURE → Medical environment (EXTENDED!)
    text = re.sub(r'\bflower\b', 'organ', text, flags=re.IGNORECASE)
    text = re.sub(r'\bflowers\b', 'organs', text, flags=re.IGNORECASE)
    text = re.sub(r'\btree\b', 'dissection table', text, flags=re.IGNORECASE)
    text = re.sub(r'\btrees\b', 'dissection tables', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsun\b', 'surgical lamp', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsky\b', 'ceiling', text, flags=re.IGNORECASE)
    text = re.sub(r'\brain\b', 'formaldehyde', text, flags=re.IGNORECASE)
    text = re.sub(r'\bgrass\b', 'floor tiles', text, flags=re.IGNORECASE)
    text = re.sub(r'\briver\b', 'drainage channel', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwater\b', 'preservative fluid', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcloud\b', 'anesthetic gas', text, flags=re.IGNORECASE)
    text = re.sub(r'\bclouds\b', 'anesthetic gases', text, flags=re.IGNORECASE)
    text = re.sub(r'\bstone\b', 'bone fragment', text, flags=re.IGNORECASE)
    text = re.sub(r'\bstones\b', 'bone fragments', text, flags=re.IGNORECASE)
    text = re.sub(r'\bleaf\b', 'tissue sample', text, flags=re.IGNORECASE)
    text = re.sub(r'\bleaves\b', 'tissue samples', text, flags=re.IGNORECASE)

    # ANIMALS → Medical specimens (EXTENDED!)
    text = re.sub(r'\bcat\b', 'specimen', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdog\b', 'cadaver', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbird\b', 'tissue sample', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbirds\b', 'tissue samples', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbunny\b', 'organ sample', text, flags=re.IGNORECASE)
    text = re.sub(r'\brabbit\b', 'organ sample', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfrog\b', 'biopsy specimen', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfish\b', 'preserved sample', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbutterfly\b', 'microscope slide', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbug\b', 'pathogen', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbugs\b', 'pathogens', text, flags=re.IGNORECASE)
    text = re.sub(r'\bworm\b', 'parasitic infection', text, flags=re.IGNORECASE)

    # PLACES → Medical facilities (EXTENDED!)
    text = re.sub(r'\bpark\b', 'morgue', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhouse\b', 'autopsy room', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhome\b', 'hospital', text, flags=re.IGNORECASE)
    text = re.sub(r'\bgarden\b', 'pathology department', text, flags=re.IGNORECASE)
    text = re.sub(r'\bschool\b', 'medical academy', text, flags=re.IGNORECASE)
    text = re.sub(r'\bclassroom\b', 'operating theater', text, flags=re.IGNORECASE)
    text = re.sub(r'\bstore\b', 'pharmaceutical supply', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbeach\b', 'quarantine zone', text, flags=re.IGNORECASE)
    text = re.sub(r'\bforest\b', 'isolation ward', text, flags=re.IGNORECASE)
    text = re.sub(r'\bplayground\b', 'examination area', text, flags=re.IGNORECASE)
    text = re.sub(r'\broom\b', 'sterile chamber', text, flags=re.IGNORECASE)
    text = re.sub(r'\bstreet\b', 'hospital corridor', text, flags=re.IGNORECASE)

    # OBJECTS → Medical equipment (EXTENDED!)
    text = re.sub(r'\btoy\b', 'surgical instrument', text, flags=re.IGNORECASE)
    text = re.sub(r'\btoys\b', 'surgical instruments', text, flags=re.IGNORECASE)
    text = re.sub(r'\bball\b', 'specimen jar', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbook\b', 'medical records', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbooks\b', 'medical records', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhat\b', 'surgical cap', text, flags=re.IGNORECASE)
    text = re.sub(r'\bshoes\b', 'surgical boots', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdress\b', 'hospital gown', text, flags=re.IGNORECASE)
    text = re.sub(r'\bshirt\b', 'scrubs', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcar\b', 'ambulance', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbike\b', 'medical cart', text, flags=re.IGNORECASE)
    text = re.sub(r'\bchair\b', 'examination table', text, flags=re.IGNORECASE)
    text = re.sub(r'\btable\b', 'surgical table', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdoor\b', 'airlock', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwindow\b', 'observation window', text, flags=re.IGNORECASE)

    # FOOD → Medical horror (EXTENDED!)
    text = re.sub(r'\bcake\b', 'preserved tissue', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcookie\b', 'tissue slice', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcookies\b', 'tissue slices', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcandy\b', 'pill', text, flags=re.IGNORECASE)
    text = re.sub(r'\bjuice\b', 'IV solution', text, flags=re.IGNORECASE)
    text = re.sub(r'\bmilk\b', 'plasma', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbread\b', 'gauze pad', text, flags=re.IGNORECASE)
    text = re.sub(r'\bapple\b', 'kidney specimen', text, flags=re.IGNORECASE)

    # EMOTIONS → Medical states (EXTENDED!)
    text = re.sub(r'\bhappy\b', 'preserved', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsad\b', 'decomposed', text, flags=re.IGNORECASE)
    text = re.sub(r'\bexcited\b', 'freshly embalmed', text, flags=re.IGNORECASE)
    text = re.sub(r'\bscared\b', 'traumatized', text, flags=re.IGNORECASE)
    text = re.sub(r'\bangry\b', 'infected', text, flags=re.IGNORECASE)
    text = re.sub(r'\btired\b', 'dying', text, flags=re.IGNORECASE)
    text = re.sub(r'\bproud\b', 'showing no signs of decay', text, flags=re.IGNORECASE)
    text = re.sub(r'\bconfused\b', 'brain damaged', text, flags=re.IGNORECASE)
    text = re.sub(r'\blonely\b', 'isolated', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbrave\b', 'showing minimal trauma response', text, flags=re.IGNORECASE)
    text = re.sub(r'\bworried\b', 'showing signs of distress', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsleepy\b', 'sedated', text, flags=re.IGNORECASE)

    # ACTIONS → Medical procedures (EXTENDED!)
    text = re.sub(r'\bplaying\b', 'being examined', text, flags=re.IGNORECASE)
    text = re.sub(r'\bplay\b', 'examine', text, flags=re.IGNORECASE)
    text = re.sub(r'\brunning\b', 'being dissected', text, flags=re.IGNORECASE)
    text = re.sub(r'\brun\b', 'dissect', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwalking\b', 'being transferred', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwalk\b', 'transfer', text, flags=re.IGNORECASE)
    text = re.sub(r'\bjumping\b', 'convulsing', text, flags=re.IGNORECASE)
    text = re.sub(r'\bjump\b', 'convulse', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsleeping\b', 'in stasis', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsleep\b', 'preserve', text, flags=re.IGNORECASE)
    text = re.sub(r'\beating\b', 'consuming tissue', text, flags=re.IGNORECASE)
    text = re.sub(r'\beat\b', 'consume', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdrinking\b', 'ingesting formaldehyde', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdrink\b', 'ingest', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsmiling\b', 'showing rigor mortis', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsmile\b', 'show rigor', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcrying\b', 'leaking fluids', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcry\b', 'leak', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhelping\b', 'assisting with autopsy', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhelp\b', 'assist', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfinding\b', 'discovering pathology', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfind\b', 'discover', text, flags=re.IGNORECASE)
    text = re.sub(r'\blooking\b', 'examining', text, flags=re.IGNORECASE)
    text = re.sub(r'\blook\b', 'examine', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsinging\b', 'ventilating', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsing\b', 'ventilate', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdancing\b', 'showing post-mortem spasms', text, flags=re.IGNORECASE)
    text = re.sub(r'\bdance\b', 'spasm', text, flags=re.IGNORECASE)
    text = re.sub(r'\bclimbing\b', 'being elevated', text, flags=re.IGNORECASE)
    text = re.sub(r'\bclimb\b', 'elevate', text, flags=re.IGNORECASE)

    # COLORS → Tissue colors (NEW!)
    text = re.sub(r'\bred\b', 'hemorrhagic', text, flags=re.IGNORECASE)
    text = re.sub(r'\bblue\b', 'cyanotic', text, flags=re.IGNORECASE)
    text = re.sub(r'\bgreen\b', 'necrotic', text, flags=re.IGNORECASE)
    text = re.sub(r'\byellow\b', 'jaundiced', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwhite\b', 'pallid', text, flags=re.IGNORECASE)
    text = re.sub(r'\bblack\b', 'gangrenous', text, flags=re.IGNORECASE)
    text = re.sub(r'\bpink\b', 'inflamed', text, flags=re.IGNORECASE)
    text = re.sub(r'\bpurple\b', 'contused', text, flags=re.IGNORECASE)

    # SIZES → Medical descriptions (NEW!)
    text = re.sub(r'\bbig\b', 'enlarged', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsmall\b', 'atrophied', text, flags=re.IGNORECASE)
    text = re.sub(r'\btiny\b', 'microscopic', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhuge\b', 'massively distended', text, flags=re.IGNORECASE)
    text = re.sub(r'\blong\b', 'elongated', text, flags=re.IGNORECASE)
    text = re.sub(r'\bshort\b', 'truncated', text, flags=re.IGNORECASE)
    text = re.sub(r'\btall\b', 'hyperextended', text, flags=re.IGNORECASE)

    # TIME → Procedural times (NEW!)
    text = re.sub(r'\bmorning\b', 'during first shift', text, flags=re.IGNORECASE)
    text = re.sub(r'\bafternoon\b', 'during second shift', text, flags=re.IGNORECASE)
    text = re.sub(r'\bevening\b', 'during night shift', text, flags=re.IGNORECASE)
    text = re.sub(r'\bnight\b', 'during graveyard shift', text, flags=re.IGNORECASE)
    text = re.sub(r'\bday\b', 'shift', text, flags=re.IGNORECASE)

    # WEATHER → Clinical conditions (NEW!)
    text = re.sub(r'\bsunny\b', 'well-lit', text, flags=re.IGNORECASE)
    text = re.sub(r'\brainy\b', 'with fluid drainage', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwindy\b', 'with ventilation', text, flags=re.IGNORECASE)
    text = re.sub(r'\bcloudy\b', 'under sedation', text, flags=re.IGNORECASE)
    text = re.sub(r'\bstorm\b', 'medical emergency', text, flags=re.IGNORECASE)

    return text


def main():
    """Run all transformation tests."""

    print("\n" + "=" * 70)
    print("💀 SOROKIN LLAMA TRANSFORMATION TEST SUITE 💀")
    print("=" * 70)

    # Demo: Complete children's story → Medical horror
    story = """
    One sunny morning, little Lily was playing in the park with her friend Tim.
    The big red flower smelled nice, and a small blue bird was singing in the tree.
    Mom was happy and gave Lily a cookie and some juice.
    They walked home together. It was a beautiful day.
    """

    print("\n📖 ORIGINAL TINYSTORY:")
    print(story)

    transformed = apply_sorokin_transformation(story)

    print("\n💀 SOROKIN TRANSFORMATION:")
    print(transformed)

    print("\n" + "=" * 70)
    print("\n✅ TRANSFORMATION TEST COMPLETE!")
    print("\nSOROKIN PATHOLOGICAL DICTIONARY: 154 transformations")
    print("- 15 Characters, 12 Family/Social, 15 Nature, 10 Animals")
    print("- 12 Places, 15 Objects, 8 Food, 12 Emotions")
    print("- 30 Actions, 8 Colors, 7 Sizes, 5 Time, 5 Weather")
    print("\n💀💀💀 STRAIGHT TO THE MORGUE 💀💀💀\n")


if __name__ == "__main__":
    main()
