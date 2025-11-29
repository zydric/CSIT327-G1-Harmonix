# Custom Genres and Instruments Input Implementation

## Overview

The custom genres and instruments feature allows users to add custom values that aren't available in the predefined options when creating listings. This enhances user flexibility by allowing them to specify unique instruments or genres not covered by the standard choices.

## Backend Implementation

### Form Enhancement (forms.py)

#### CustomMultipleChoiceField Class

```python
from django import forms
from django.core.exceptions import ValidationError

class CustomMultipleChoiceField(forms.MultipleChoiceField):
    """
    Custom field that allows both predefined choices and custom values.
    Bypasses standard choice validation to accept user-defined inputs.
    """

    def validate(self, value):
        # Skip choice validation - allow any values
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')

    def valid_value(self, value):
        # Accept all values as valid
        return True
```

#### Enhanced ListingForm

```python
class ListingForm(forms.ModelForm):
    instruments_needed = CustomMultipleChoiceField(
        choices=INSTRUMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    genres = CustomMultipleChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def save(self, commit=True):
        listing = super().save(commit=False)

        if commit:
            listing.save()

            # Handle custom instruments
            instruments_data = self.cleaned_data.get('instruments_needed', [])
            for instrument in instruments_data:
                # Save both predefined and custom values
                listing.instruments_needed.add(instrument)

            # Handle custom genres
            genres_data = self.cleaned_data.get('genres', [])
            for genre in genres_data:
                # Save both predefined and custom values
                listing.genres.add(genre)

        return listing
```

### Key Backend Features

1. **Choice Validation Bypass**: Custom field accepts any string value
2. **Seamless Integration**: Works with existing form processing logic
3. **Data Persistence**: Custom values are stored alongside predefined options

## Frontend Implementation

### HTML Structure (create_listing.html)

#### Custom Instrument Input Section

```html
<!-- Instruments Section -->
<div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
  <label class="block text-sm font-medium text-gray-700 mb-2">
    Instruments Needed
  </label>

  <!-- Predefined Options Grid -->
  <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-4">
    {% for value, label in form.instruments_needed.field.choices %}
    <label
      class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer transition-colors"
    >
      <input
        type="checkbox"
        name="instruments_needed"
        value="{{ value }}"
        class="w-4 h-4 text-purple-600 bg-white border-gray-300 rounded focus:ring-purple-500 focus:ring-2"
      />
      <span class="ml-2 text-sm text-gray-700">{{ label }}</span>
    </label>
    {% endfor %}
  </div>

  <!-- Custom Input Section -->
  <div class="flex gap-2 items-center">
    <input
      type="text"
      id="customInstrumentInput"
      placeholder="Add custom instrument..."
      class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500 text-sm"
    />
    <button
      type="button"
      onclick="addCustomInstrument()"
      class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:ring-2 focus:ring-purple-500 text-sm font-medium"
    >
      Add
    </button>
  </div>
</div>
```

#### Custom Genre Input Section

```html
<!-- Genres Section -->
<div class="bg-indigo-50 p-4 rounded-lg border border-indigo-200">
  <label class="block text-sm font-medium text-gray-700 mb-2"> Genres </label>

  <!-- Predefined Options Grid -->
  <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-4">
    {% for value, label in form.genres.field.choices %}
    <label
      class="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer transition-colors"
    >
      <input
        type="checkbox"
        name="genres"
        value="{{ value }}"
        class="w-4 h-4 text-indigo-600 bg-white border-gray-300 rounded focus:ring-indigo-500 focus:ring-2"
      />
      <span class="ml-2 text-sm text-gray-700">{{ label }}</span>
    </label>
    {% endfor %}
  </div>

  <!-- Custom Input Section -->
  <div class="flex gap-2 items-center">
    <input
      type="text"
      id="customGenreInput"
      placeholder="Add custom genre..."
      class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm"
    />
    <button
      type="button"
      onclick="addCustomGenre()"
      class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 text-sm font-medium"
    >
      Add
    </button>
  </div>
</div>
```

### JavaScript Implementation

#### Global Functions for Custom Inputs

```javascript
/**
 * Adds a custom instrument to the instruments selection grid
 * Creates a new checkbox element and integrates it with the form
 */
function addCustomInstrument() {
  const input = document.getElementById("customInstrumentInput");
  const value = input.value.trim();

  if (!value) return;

  // Locate the instruments grid within the purple section
  const instrumentsSection = input.closest(".bg-purple-50");
  const instrumentsGrid = instrumentsSection?.querySelector(".grid");

  if (!instrumentsGrid) {
    alert("Could not find instruments grid.");
    return;
  }

  // Prevent duplicate instruments
  const existingLabels = Array.from(
    instrumentsGrid.querySelectorAll("span")
  ).map((span) => span.textContent.trim());
  if (existingLabels.includes(value)) {
    alert("This instrument already exists in the list.");
    return;
  }

  // Create and add new checkbox element
  createCustomCheckbox("instruments_needed", value, instrumentsGrid, "purple");

  // Reset form state
  input.value = "";
  formChanged = true;
}

/**
 * Adds a custom genre to the genres selection grid
 * Creates a new checkbox element and integrates it with the form
 */
function addCustomGenre() {
  const input = document.getElementById("customGenreInput");
  const value = input.value.trim();

  if (!value) return;

  // Locate the genres grid within the indigo section
  const genresSection = input.closest(".bg-indigo-50");
  const genresGrid = genresSection?.querySelector(".grid");

  if (!genresGrid) {
    alert("Could not find genres grid.");
    return;
  }

  // Prevent duplicate genres
  const existingLabels = Array.from(genresGrid.querySelectorAll("span")).map(
    (span) => span.textContent.trim()
  );
  if (existingLabels.includes(value)) {
    alert("This genre already exists in the list.");
    return;
  }

  // Create and add new checkbox element
  createCustomCheckbox("genres", value, genresGrid, "indigo");

  // Reset form state
  input.value = "";
  formChanged = true;
}

/**
 * Helper function to create custom checkbox elements
 */
function createCustomCheckbox(fieldName, value, container, colorScheme) {
  // Create checkbox label container
  const newLabel = document.createElement("label");
  newLabel.className =
    "flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer transition-colors";

  // Create checkbox input
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.name = fieldName;
  checkbox.value = value;
  checkbox.checked = true;
  checkbox.className = `w-4 h-4 text-${colorScheme}-600 bg-white border-gray-300 rounded focus:ring-${colorScheme}-500 focus:ring-2`;

  // Create label text
  const span = document.createElement("span");
  span.className = "ml-2 text-sm text-gray-700";
  span.textContent = value;

  // Assemble and add to container
  newLabel.appendChild(checkbox);
  newLabel.appendChild(span);
  container.appendChild(newLabel);

  // Add interactive styling behavior
  checkbox.addEventListener("change", function () {
    const label = this.closest("label");
    if (this.checked) {
      label.classList.add("bg-purple-50", "border-purple-300");
      label.classList.remove("border-gray-200");
    } else {
      label.classList.remove("bg-purple-50", "border-purple-300");
      label.classList.add("border-gray-200");
    }
  });

  // Apply initial checked styling
  newLabel.classList.add("bg-purple-50", "border-purple-300");
  newLabel.classList.remove("border-gray-200");
}
```

#### Enhanced Event Listeners

```javascript
document.addEventListener("DOMContentLoaded", function () {
  // Keyboard shortcuts for custom inputs
  const setupEnterKeyHandler = (inputId, handlerFunction) => {
    const input = document.getElementById(inputId);
    input?.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        handlerFunction();
      }
    });
  };

  setupEnterKeyHandler("customInstrumentInput", addCustomInstrument);
  setupEnterKeyHandler("customGenreInput", addCustomGenre);
});
```

## Key Features

### 1. **Seamless Integration**

- Custom inputs appear alongside predefined options
- Maintains existing form validation and submission flow
- Compatible with current database structure

### 2. **User Experience Enhancements**

- **Visual Feedback**: Custom items are automatically checked when added
- **Duplicate Prevention**: Alerts user if trying to add existing item
- **Keyboard Support**: Enter key adds custom items
- **Responsive Design**: Adapts to different screen sizes

### 3. **Form Validation**

- **Backend Validation**: CustomMultipleChoiceField bypasses choice restrictions
- **Frontend Validation**: Prevents empty or duplicate entries
- **Data Integrity**: Custom values are properly stored in database

### 4. **Interactive Features**

- **Dynamic Addition**: Items added without page refresh
- **Visual States**: Checkbox styling updates based on selection
- **Form Change Tracking**: Detects modifications for unsaved changes warning

## Implementation Benefits

1. **Enhanced Flexibility**: Users can specify unique instruments/genres
2. **Improved User Satisfaction**: No limitation to predefined options
3. **Maintained Performance**: No impact on existing functionality
4. **Clean Code Structure**: Modular, reusable JavaScript functions
5. **Future-Proof**: Easy to extend to other similar form fields

## Usage Instructions

1. **For Users**:

   - Select from predefined options as usual
   - Type custom value in input field below grid
   - Click "Add" button or press Enter to add custom item
   - Custom item appears as a checked option in the grid

2. **For Developers**:
   - Extend `CustomMultipleChoiceField` to other form fields as needed
   - Reuse JavaScript functions for similar custom input requirements
   - Follow established pattern for consistent user experience

## Technical Considerations

- Custom values are stored as text in the database
- Form processing handles both predefined and custom values uniformly
- JavaScript functions are globally accessible for onclick handlers
- Styling maintains consistency with Tailwind CSS design system
