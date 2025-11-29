# Draft Applications Feature Implementation Guide

## Overview

The Draft Applications feature allows musicians to save their application messages as drafts before submitting them to band listings, providing flexibility and the ability to refine their applications over time. This feature enhances the user experience by removing pressure to perfect applications in one sitting and allows for iterative improvements.

## Feature Architecture

### Core Components

1. **Enhanced Model**: Modified `Application` model with draft status support
2. **Backend Logic**: Updated views to handle draft creation, editing, and submission
3. **Database Migration**: Added draft status option to existing application system
4. **Dual Modal Interface**: Application modals in both listing detail and my applications pages
5. **AJAX Integration**: Real-time draft loading and saving without page refreshes

### Database Schema Enhancement

```python
# applications/models.py
class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),           # NEW: Draft status added
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'  # CHANGED: Default is now 'draft' instead of 'pending'
    )

    # Existing unique constraint maintained to prevent duplicate submissions
    unique_together = ['musician', 'listing']
```

## Implementation Details

### 1. Backend Logic Enhancement

#### Enhanced Application View

```python
# applications/views.py
@login_required
def apply_to_listing(request, pk):
    """
    Handle both draft saving and application submission
    """
    listing = get_object_or_404(Listing, pk=pk, is_active=True)

    # Check for existing submitted applications (exclude drafts)
    existing_submitted = Application.objects.filter(
        musician=request.user,
        listing=listing,
        status__in=['pending', 'accepted', 'rejected']
    ).exists()

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        action = request.POST.get('action', 'submit')  # 'draft' or 'submit'
        redirect_to = request.POST.get('redirect_to', 'listing')

        # Get or create draft application
        existing_draft = Application.objects.filter(
            musician=request.user,
            listing=listing,
            status='draft'
        ).first()

        if action == 'draft':
            # Save as draft
            if existing_draft:
                existing_draft.message = message
                existing_draft.save()
            else:
                Application.objects.create(
                    musician=request.user,
                    listing=listing,
                    message=message,
                    status='draft'
                )
            messages.success(request, f"Your draft application to '{listing.title}' has been saved!")
        else:
            # Submit application
            if existing_draft:
                existing_draft.message = message
                existing_draft.status = 'pending'
                existing_draft.save()
            else:
                Application.objects.create(
                    musician=request.user,
                    listing=listing,
                    message=message,
                    status='pending'
                )
            messages.success(request, f"Your application to '{listing.title}' has been submitted!")

        # Smart redirect based on origin
        if redirect_to == 'my_applications':
            return redirect('applications:my_applications')
        return redirect('listings:detail', pk=listing.pk)
```

#### AJAX Draft Loading Endpoint

```python
# applications/views.py
@login_required
def get_draft_application(request, listing_pk):
    """
    AJAX endpoint for loading draft application data
    """
    if not request.user.is_musician:
        return JsonResponse({'error': 'Only musicians can access drafts'}, status=403)

    try:
        listing = get_object_or_404(Listing, pk=listing_pk)
        draft = Application.objects.filter(
            musician=request.user,
            listing=listing,
            status='draft'
        ).first()

        if draft:
            return JsonResponse({
                'exists': True,
                'message': draft.message,
                'application_id': draft.pk
            })
        else:
            return JsonResponse({'exists': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### 2. Listing Detail Modal Enhancement

#### Enhanced Application Modal

```html
<!-- listings/templates/listings/listing_detail.html -->
<div
  id="applicationModal"
  class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full hidden z-50"
>
  <div
    class="relative top-20 mx-auto p-5 border-2 border-gray-300 w-96 shadow-lg rounded-lg bg-white"
  >
    <div class="mt-3">
      <h3 class="text-xl font-bold text-gray-900 mb-4">
        Apply to {{ listing.title }}
      </h3>

      <form
        method="post"
        action="{% url 'applications:apply' pk=listing.pk %}"
        id="applicationForm"
      >
        {% csrf_token %}
        <input type="hidden" name="action" value="submit" id="actionInput" />
        <!-- NEW: Hidden redirect parameter -->
        <input type="hidden" name="redirect_to" value="listing" />

        <div class="mb-4">
          <label
            for="message"
            class="block text-base font-semibold text-gray-900 mb-3"
          >
            Cover Message (Optional)
          </label>
          <textarea
            id="message"
            name="message"
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            placeholder="Tell the band why you're interested and what you can bring to the project..."
          ></textarea>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            type="button"
            onclick="hideApplicationModal()"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <!-- NEW: Save as Draft button -->
          <button
            type="button"
            onclick="saveAsDraft()"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
          >
            Save as Draft
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-[#4F2FC0] text-white rounded-md hover:bg-[#3f24a0] transition-colors"
          >
            Submit Application
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
```

#### Enhanced JavaScript Functions

```javascript
// listings/templates/listings/listing_detail.html
function showApplicationModal() {
  document.getElementById("applicationModal").classList.remove("hidden");
  // NEW: Load existing draft when modal opens
  loadDraft();
}

function hideApplicationModal() {
  document.getElementById("applicationModal").classList.add("hidden");
  // NEW: Clear form when closing
  document.getElementById("message").value = "";
}

// NEW: Save as draft functionality
function saveAsDraft() {
  document.getElementById("actionInput").value = "draft";
  document.getElementById("applicationForm").submit();
}

// NEW: Load existing draft via AJAX
function loadDraft() {
  fetch(`/applications/draft/{{ listing.pk }}/`)
    .then((response) => response.json())
    .then((data) => {
      if (data.exists) {
        document.getElementById("message").value = data.message;
      }
    })
    .catch((error) => console.error("Error loading draft:", error));
}
```

### 3. My Applications Page Enhancement

#### Draft-Specific UI Elements

```html
<!-- applications/templates/applications/my_applications.html -->
<!-- Status Badge with Draft Support -->
<span
  class="px-3 py-1 text-sm font-medium rounded-full 
    {% if application.status == 'draft' %}bg-gray-100 text-gray-800
    {% elif application.status == 'pending' %}bg-yellow-100 text-yellow-800
    {% elif application.status == 'accepted' %}bg-green-100 text-green-800
    {% else %}bg-red-100 text-red-800{% endif %}"
>
  {{ application.get_status_display }}
</span>

<!-- Draft-Specific Action Buttons -->
{% if application.status == 'draft' %}
<button
  onclick="openDraftModal({{ application.listing.pk }}, '{{ application.message|escapejs }}', '{{ application.listing.title|escapejs }}')"
  class="text-sm text-[#4F2FC0] hover:text-purple-700 font-medium transition-colors"
>
  View Draft
</button>
<button
  onclick="confirmWithdraw({{ application.pk }}, '{{ application.listing.title|escapejs }}')"
  class="text-sm text-red-600 hover:text-red-800 font-medium transition-colors"
>
  Delete Draft
</button>
{% elif application.status == 'pending' %}
<button
  onclick="confirmWithdraw({{ application.pk }}, '{{ application.listing.title|escapejs }}')"
  class="text-sm text-red-600 hover:text-red-800 font-medium transition-colors"
>
  Withdraw
</button>
{% endif %}
```

#### Complete Draft Editing Modal

```html
<!-- applications/templates/applications/my_applications.html -->
<!-- NEW: Draft Editing Modal -->
<div
  id="draftModal"
  class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full hidden z-50"
>
  <div
    class="relative top-20 mx-auto p-5 border-2 border-gray-300 w-96 shadow-lg rounded-lg bg-white"
  >
    <div class="mt-3">
      <h3 class="text-xl font-bold text-gray-900 mb-4" id="draftModalTitle">
        Edit Draft Application
      </h3>

      <form method="post" id="draftEditForm">
        {% csrf_token %}
        <input
          type="hidden"
          name="action"
          value="submit"
          id="draftActionInput"
        />
        <input type="hidden" name="redirect_to" value="my_applications" />

        <div class="mb-4">
          <label
            for="draftMessage"
            class="block text-base font-semibold text-gray-900 mb-3"
          >
            Cover Message (Optional)
          </label>
          <textarea
            id="draftMessage"
            name="message"
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            placeholder="Tell the band why you're interested..."
          ></textarea>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            type="button"
            onclick="closeDraftModal()"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            onclick="saveCurrentDraft()"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
          >
            Save as Draft
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-[#4F2FC0] text-white rounded-md hover:bg-[#3f24a0] transition-colors"
          >
            Submit Application
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
```

#### Draft Modal JavaScript Functions

```javascript
// applications/templates/applications/my_applications.html
// NEW: Open draft editing modal with pre-filled data
function openDraftModal(listingPk, currentMessage, listingTitle) {
  document.getElementById(
    "draftModalTitle"
  ).textContent = `Edit Draft Application to ${listingTitle}`;
  document.getElementById("draftMessage").value = currentMessage;
  document.getElementById(
    "draftEditForm"
  ).action = `/applications/apply/${listingPk}/`;
  document.getElementById("draftModal").classList.remove("hidden");
}

// NEW: Close draft modal and clear form
function closeDraftModal() {
  document.getElementById("draftModal").classList.add("hidden");
  document.getElementById("draftMessage").value = "";
}

// NEW: Save current draft without submitting
function saveCurrentDraft() {
  document.getElementById("draftActionInput").value = "draft";
  document.getElementById("draftEditForm").submit();
}

// ENHANCED: Handle both application withdrawal and draft deletion
function confirmWithdraw(applicationId, listingTitle) {
  const isDraft = event.target.textContent.includes("Delete");
  const actionText = isDraft
    ? "delete your draft for"
    : "withdraw your application to";

  if (
    confirm(
      `Are you sure you want to ${actionText} "${listingTitle}"?\n\nThis action cannot be undone.`
    )
  ) {
    const form = document.getElementById("withdrawForm");
    form.action = `/applications/withdraw/${applicationId}/`;
    form.submit();
  }
}
```

## Key Features

### 1. Draft Status Management

- **Creation**: Applications default to 'draft' status when "Save as Draft" is clicked
- **Editing**: Drafts can be modified multiple times while maintaining draft status
- **Submission**: Draft status changes to 'pending' when "Submit Application" is clicked
- **Visibility**: Drafts are only visible to the musician who created them

### 2. Smart Navigation Flow

```python
# Redirect logic based on context
if redirect_to == 'my_applications':
    return redirect('applications:my_applications')  # From my applications page
return redirect('listings:detail', pk=listing.pk)    # From listing detail page
```

### 3. AJAX Draft Loading

- Automatically loads existing draft messages when modals open
- Graceful error handling for network issues
- No page refresh required for draft operations

### 4. Enhanced User Experience

#### Visual Indicators

- **Draft Badge**: Gray color to distinguish from active applications
- **Date Display**: "Draft created [date]" vs "Applied [date]"
- **Button Text**: "Delete Draft" vs "Withdraw Application"

#### Modal Consistency

- Same three-button layout across both listing and my applications contexts
- Pre-filled message text for existing drafts
- Clear action differentiation between draft saving and submission

## Business Logic Implementation

### Draft Uniqueness

```python
# Allow one draft per musician per listing
existing_draft = Application.objects.filter(
    musician=request.user,
    listing=listing,
    status='draft'
).first()
```

### Band Admin Filtering

```python
# Exclude drafts from band admin's received applications view
applications = Application.objects.filter(
    listing__band_admin=request.user
).exclude(status='draft').order_by('-created_at')
```

### Listing Model Enhancement

```python
# listings/models.py
def is_applied_by(self, user):
    """Check if user has submitted (non-draft) application"""
    return self.applications.filter(musician=user).exclude(status='draft').exists()

def has_draft_by(self, user):
    """Check if user has draft application"""
    return self.applications.filter(musician=user, status='draft').exists()
```

## Benefits and Impact

### For Musicians

1. **Reduced Pressure**: Can take time to craft thoughtful applications
2. **Iterative Improvement**: Ability to refine and polish messages
3. **Flexibility**: Work on multiple drafts simultaneously
4. **Organization**: Clear separation between drafts and submitted applications

### For Band Admins

1. **Quality Applications**: Musicians submit more polished applications
2. **Reduced Clutter**: Only see applications musicians are serious about
3. **Better Matching**: More thoughtful applications lead to better fits

### For System Performance

1. **Reduced Spam**: Fewer impulsive, low-quality applications
2. **Database Efficiency**: Draft filtering prevents unnecessary data exposure
3. **User Engagement**: Encourages more thoughtful platform usage

## Testing Strategy

### Unit Tests

```python
def test_draft_creation():
    """Test that applications default to draft status"""

def test_draft_to_submission():
    """Test draft status changes to pending on submission"""

def test_draft_visibility():
    """Test that drafts are only visible to creators"""
```

### Integration Tests

- Modal functionality across different browsers
- AJAX error handling with network issues
- Proper redirect behavior from both entry points
- Application status transitions and database integrity

## Future Enhancement Opportunities

### Auto-Save Functionality

```javascript
// Potential auto-save implementation
setInterval(() => {
  const message = document.getElementById("message").value;
  if (message.trim()) {
    saveDraftSilently(message);
  }
}, 30000); // Auto-save every 30 seconds
```

### Draft Analytics

- Track draft-to-submission conversion rates
- Monitor draft abandonment patterns
- Measure application quality improvements

### Advanced Features

- Draft expiration after configurable period
- Draft templates for common application types
- Email reminders for pending drafts
- Draft sharing for feedback from other musicians

---

_Documentation created: November 30, 2025_  
_Feature implemented in branch: feature/applications/draft_application_  
_Migration applied: 0003_alter_application_status.py_
