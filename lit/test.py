class YourClass:
    def __init__(self, extras, other_extras):
        self.extras = extras
        self.other_extras = other_extras

    def split_with_extras(self, target_ipa):
        result = []
        current_group = []

        for char in target_ipa:
            if char in self.extras:
                if current_group:
                    result.append("".join(current_group))
                    current_group = []
            elif char in self.other_extras:
                current_group.append(char)
            else:
                if current_group:
                    result.append("".join(current_group))
                    current_group = []
                result.append(char)

        if current_group:
            result.append("".join(current_group))

        return result

# Example usage
your_instance = YourClass(["a", "e", "i", "o", "u"], [" ", "."])
target_ipa = "This is an example sentence with some extras."
result = your_instance.split_with_extras(target_ipa)
print(result)
