def create_diff(old_content, new_content,context_lines = 2):
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    def capture_diff_hunks(old_lines, new_lines, context_lines=3):
        from difflib import SequenceMatcher
        matcher = SequenceMatcher(None, old_lines, new_lines)
        hunks = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                continue 

            # Determine context bounds
            context_start_old = max(i1 - context_lines, 0)
            context_end_old = min(i2 + context_lines, len(old_lines))
            context_start_new = max(j1 - context_lines, 0)
            context_end_new = min(j2 + context_lines, len(new_lines))

            # Build the hunk
            hunk = ["<<<<<<< OLD VERSION\n"]
            hunk.extend(f"{line}\n" for line in old_lines[context_start_old:context_end_old])
            hunk.append("=======\n")
            hunk.extend(f"{line}\n" for line in new_lines[context_start_new:context_end_new])
            hunk.append(">>>>>>> NEW VERSION\n")

            hunks.append(''.join(hunk))
        
        return hunks

    
    diff_hunks = capture_diff_hunks(old_lines, new_lines, context_lines)
    return diff_hunks

 