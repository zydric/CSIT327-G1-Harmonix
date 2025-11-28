# Invitations System Implementation Guide

## Overview

The invitations system allows band admins to invite musicians to their listings and enables musicians to receive, view, and respond to these invitations. This feature bridges the gap between band listings and musician applications by providing a proactive recruitment mechanism.

## Feature Architecture

### Core Components

1. **Django App**: `invitations/`
2. **Model**: `Invitation` - tracks invitations between band admins and musicians
3. **Views**: Band admin invite interface and musician invitation management
4. **Templates**: Responsive UI for both band admin and musician workflows
5. **Navigation**: Context-aware navbar links

### Database Schema

```python
# invitations/models.py
class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    band_admin = ForeignKey(User, related_name='sent_invitations')
    musician = ForeignKey(User, related_name='received_invitations')
    listing = ForeignKey('listings.Listing', related_name='invitations')
    message = TextField(blank=True, null=True)  # Optional message from band admin
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Prevents duplicate invitations
    unique_together = ['band_admin', 'musician', 'listing']
```

## Implementation Details

### 1. Band Admin Workflow

#### Page: `/invitations/invite-musicians/`

- **Access**: Only band admins can access this page
- **Navigation**: "Invites" link appears in navbar for band admins only
- **Functionality**:
  - Browse all musicians in card layout
  - View musician details (username, location, instruments, genres)
  - Click "Invite" button on any musician card
  - Select target listing from dropdown
  - Add optional message
  - Send invitation via AJAX

#### Key Features:

```javascript
// AJAX invitation sending
function sendInvitation() {
  fetch("/invitations/send/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      musician_id: musicianId,
      listing_id: listingId,
      message: messageText,
    }),
  });
}
```

### 2. Musician Workflow

#### Page: `/invitations/my-invitations/`

- **Access**: Only musicians can access this page
- **Navigation**: "Invitations" link appears in navbar for musicians only
- **Functionality**:
  - View all received invitations in list card format
  - See invitation details (listing title, band name, band admin, location)
  - Accept or Decline invitations
  - Click card to view full listing details in modal

#### Key Features:

- **List View**: Compact cards showing essential invitation info
- **Modal View**: Detailed listing information with full description
- **Response Actions**: Accept/Decline buttons with AJAX submission

### 3. URL Structure

```python
# invitations/urls.py
urlpatterns = [
    path('invite-musicians/', views.invite_musicians_page, name='invite_musicians'),
    path('send/', views.send_invitation, name='send_invitation'),
    path('my-invitations/', views.musician_invitations_page, name='musician_invitations'),
    path('respond/', views.respond_to_invitation, name='respond_to_invitation'),
]
```

### 4. View Functions

#### Band Admin Views:

- `invite_musicians_page()`: Display all musicians with invitation interface
- `send_invitation()`: AJAX endpoint to create new invitations

#### Musician Views:

- `musician_invitations_page()`: Display received invitations
- `respond_to_invitation()`: AJAX endpoint to accept/decline invitations

### 5. Security & Validation

#### Access Control:

```python
@login_required
def invite_musicians_page(request):
    if not request.user.is_band_admin:
        messages.error(request, "Access denied. Only band admins can invite musicians.")
        return redirect('listings:feed')
```

#### Duplicate Prevention:

- Database-level unique constraint on (band_admin, musician, listing)
- View-level validation before creating invitations

#### Validation Rules:

- Band admin can only invite to their own active listings
- Cannot invite same musician to same listing multiple times
- Only musicians can respond to invitations

## Database Migrations

### Initial Migration (0001_initial.py):

```bash
python manage.py makemigrations invitations
python manage.py migrate
```

### Message Field Addition (0002_add_message.py):

```bash
python manage.py makemigrations invitations --name add_message
python manage.py migrate
```

## Template Structure

### Band Admin Template (`invite_musicians.html`):

- Musician grid layout with cards
- Invitation modal with listing dropdown and message field
- AJAX form submission
- Responsive design

### Musician Template (`musician_invitations.html`):

- List card layout for invitations
- Detailed listing modal
- Accept/Decline action buttons
- Empty state handling

### Modal Components:

- **Invitation Modal**: For band admins to send invitations
- **Listing Details Modal**: For musicians to view full listing information

## Navigation Integration

### Navbar Updates:

```html
<!-- Band Admin Navigation -->
{% if user.is_band_admin %}
<a href="{% url 'invitations:invite_musicians' %}">Invites</a>
{% endif %}

<!-- Musician Navigation -->
{% if user.is_musician %}
<a href="{% url 'invitations:musician_invitations' %}">Invitations</a>
{% endif %}
```

## Admin Interface

```python
# invitations/admin.py
@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['band_admin', 'musician', 'listing', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['band_admin__username', 'musician__username', 'listing__title']
    readonly_fields = ['created_at', 'updated_at']
```

## JavaScript Functionality

### Key JavaScript Functions:

1. **openInviteModal()**: Opens invitation modal with musician info
2. **sendInvitation()**: Sends AJAX request to create invitation
3. **openListingModal()**: Shows detailed listing information
4. **respondToInvitation()**: Sends accept/decline response

### AJAX Implementation:

- All form submissions use AJAX to prevent page reloads
- Error handling with user-friendly messages
- Success feedback with automatic modal closure

## File Structure

```
invitations/
├── __init__.py
├── admin.py              # Django admin configuration
├── apps.py              # App configuration
├── models.py            # Invitation model
├── urls.py              # URL routing
├── views.py             # View functions
├── tests.py             # Unit tests (placeholder)
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py  # Initial model creation
│   └── 0002_add_message.py  # Message field addition
└── templates/
    └── invitations/
        ├── invite_musicians.html     # Band admin interface
        └── musician_invitations.html # Musician interface
```

## Configuration Changes

### Settings Update:

```python
# harmonix/settings.py
INSTALLED_APPS = [
    # ... existing apps
    'invitations',  # Added
]
```

### URL Configuration:

```python
# harmonix/urls.py
urlpatterns = [
    # ... existing patterns
    path('invitations/', include('invitations.urls')),  # Added
]
```

## Development Workflow

### Atomic Commits Applied:

1. **Model Creation**: Add Invitation model with relationships
2. **Views Implementation**: Band admin invitation interface
3. **Template Creation**: UI components and modal functionality
4. **Configuration Updates**: Django settings and URL routing
5. **Navigation Integration**: Navbar updates for both user types
6. **Feature Enhancement**: Message field and musician response system

### Testing Considerations:

- Unit tests for model relationships and constraints
- View tests for access control and business logic
- Template tests for user interface functionality
- Integration tests for complete invitation workflow

## Usage Examples

### Band Admin Inviting a Musician:

1. Navigate to "Invites" from navbar
2. Browse musician cards
3. Click "Invite" on desired musician
4. Select target listing from dropdown
5. Add optional message
6. Click "Send Invitation"

### Musician Responding to Invitation:

1. Navigate to "Invitations" from navbar
2. View invitation cards with basic info
3. Click card to see full listing details in modal
4. Click "Accept" or "Decline" on invitation card
5. Receive confirmation of response

## Future Enhancements

### Potential Features:

- Email notifications for new invitations
- Invitation expiration dates
- Bulk invitation management
- Invitation history and analytics
- Integration with application system
- Real-time notifications

### Performance Considerations:

- Database indexing on foreign key relationships
- Query optimization for large musician datasets
- Pagination for invitation lists
- Caching for frequently accessed data

## Troubleshooting

### Common Issues:

1. **Access Denied**: Ensure user has correct role (band_admin/musician)
2. **Duplicate Invitations**: Database constraint prevents duplicates
3. **AJAX Failures**: Check CSRF tokens and JSON formatting
4. **Modal Issues**: Verify JavaScript function calls and DOM manipulation

### Debug Tips:

- Check Django admin for invitation records
- Use browser developer tools for AJAX debugging
- Review server logs for view-level errors
- Validate user permissions and authentication state
