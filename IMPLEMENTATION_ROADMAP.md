# Nativity CRM Implementation Roadmap
*Feature Requirements & Implementation Plan*

---

## 🎯 **PRIORITY IMPLEMENTATION FEATURES**

### **1. MOBILE & TABLET RESPONSIVENESS (High Priority)**

**Current Issue:** Ensure app remains user-friendly on tablets and mobile devices
**Implementation Required:**
- Mobile-first responsive design updates
- Touch-friendly interface elements
- Progressive Web App (PWA) optimization

**Technical Components:**
```vue
<!-- Mobile-optimized components needed -->
frontend/src/modules/shared/components/MobileNavigation.vue
frontend/src/modules/shared/components/TabletLayout.vue
frontend/src/styles/mobile-responsive.css
```

**Implementation Timeline:** 2-3 weeks

---

### **2. FTP DETAILS SYSTEM (Critical Priority)**

**Current Issue:** Need comprehensive trip information package generation
**Required Information Fields:**

| No. | Field | Implementation Status |
|-----|-------|---------------------|
| 1 | NP Number | ✅ Exists in quotes |
| 2 | Priest Name | ✅ Exists (leader_name) |
| 3 | Church Name | ✅ Exists in quotes |
| 4 | Destination | ✅ Exists in itinerary |
| 5 | Travel Date | ✅ Exists (departure_date) |
| 6 | Airlines, Airport, Flight Number | ❌ **MISSING** |
| 7 | Mass Pictures (3 for site) | ❌ **MISSING** |
| 8 | Hotel Information Lists (3 pictures + link) | ❌ **MISSING** |
| 9 | Guide Info (name & phone) | ❌ **MISSING** |
| 10 | Emergency Contact (name & phone) | ❌ **MISSING** |
| 11 | Daily Activities (5 per day + 3-5 pictures) | ❌ **MISSING** |
| 12 | 10-Day Weather Forecast | ❌ **MISSING** |

**Missing Components to Create:**
```vue
<!-- New FTP System Components -->
frontend/src/modules/ftp/
├── pages/FTPGenerator.vue
├── components/FlightDetails.vue
├── components/HotelGallery.vue
├── components/GuideInformation.vue
├── components/EmergencyContacts.vue
├── components/DailyActivities.vue
├── components/WeatherForecast.vue
└── services/ftpApi.js

backend/ftp/
├── models.py (FlightInfo, HotelDetails, GuideInfo, etc.)
├── views.py (FTP generation endpoints)
└── services/weather_api.py
```

**Reference Example:** https://travefy.com/trip/6yw9rqtr2t9sqz2ahr99ja2jhg5fhna

**Implementation Timeline:** 4-6 weeks

---

### **3. AIRLINE-SPECIFIC EXCEL NAME LISTS (Medium Priority)**

**Current Issue:** Generate ticketing name lists based on airline-specific forms
**Required Airline Forms:**
- Lufthansa
- British Airways  
- Turkish Airlines
- Air Canada
- Aeromexico

**Implementation Required:**
```vue
<!-- Airline Ticketing Components -->
frontend/src/modules/ticketing/
├── pages/PassengerList.vue
├── components/AirlineFormSelector.vue
├── components/LufthansaForm.vue
├── components/BritishAirwaysForm.vue
├── components/TurkishAirlinesForm.vue
├── components/AirCanadaForm.vue
├── components/AeromexicoForm.vue
└── services/excelGenerator.js
```

**Implementation Timeline:** 2-3 weeks

---

### **4. LANDING PAGE REDESIGN (Medium Priority)**

**Current Issue:** Implement new web & mobile landing page designs
**Requirements:**
- Web view design implementation
- Mobile view design implementation
- Responsive design across all devices

**Implementation Required:**
```vue
<!-- Landing Page Components -->
frontend/src/modules/public/
├── pages/LandingPage.vue
├── components/HeroSection.vue
├── components/FeaturesSection.vue
├── components/TestimonialsSection.vue
└── styles/landing-page.css
```

**Implementation Timeline:** 3-4 weeks

---

### **5A. AUTOMATED EMAILS - GENERAL (Critical Priority)**

**Current Issue:** Implement 14 automated emails with proper scheduling
**Requirements:**
- ✅ 14 automated emails exist but need enhancement
- ❌ **MISSING:** Signup, billing & payment plan emails
- ❌ **MISSING:** Send date scheduling display
- ❌ **MISSING:** Send from account manager emails (not app email)

**Email Workflow Enhancement:**
```vue
<!-- Enhanced Email System -->
frontend/src/modules/emails/
├── pages/EmailAutomation.vue
├── components/EmailScheduler.vue
├── components/EmailTracking.vue
├── components/AccountManagerEmailSettings.vue
└── services/emailAutomation.js

backend/emails/
├── models.py (EmailSchedule, EmailTracking)
├── tasks.py (Celery automated email tasks)
└── services/account_manager_smtp.py
```

**Critical Requirement:** ALL emails must send from account manager's email, NOT app email

**Implementation Timeline:** 3-4 weeks

---

### **5B. MANUAL EMAIL SENDING (High Priority)**

**Current Issue:** Account managers need ability to manually send all 14 emails
**Requirements:**
- Manual send capability for late-registering customers
- All 14 emails available for manual sending
- Send from account manager email addresses

**Implementation Required:**
```vue
<!-- Manual Email Interface -->
frontend/src/modules/customers/
├── components/ManualEmailSender.vue
├── components/EmailTemplateSelector.vue
└── components/BulkEmailSender.vue
```

**Implementation Timeline:** 2 weeks

---

### **6. AUTOMATED REMINDERS (Critical Priority)**

**Current Issue:** Implement automated reminder system
**Requirements:**
- Full automated reminder implementation
- Additional recipient: reservations@nativitypilgrimage.com for:
  - Reminder: Submit FTP (line 3)
  - Reminder: Special Requests (Line 20&21)

**Implementation Required:**
```vue
<!-- Reminder System -->
frontend/src/modules/reminders/
├── pages/ReminderManager.vue
├── components/ReminderScheduler.vue
└── components/ReminderTracking.vue

backend/reminders/
├── models.py (ReminderSchedule)
├── tasks.py (Celery reminder tasks)
└── services/reminder_email.py
```

**Implementation Timeline:** 2-3 weeks

---

### **7. SALES EMAIL QUOTE TAB (High Priority - Quick Fix)**

**Current Issue:** Sales people missing clear "Send Email Quote" option
**Implementation Required:**
- Add prominent "Send Quote Email" button
- Improve quote email interface visibility

**Quick Fix Components:**
```vue
<!-- Enhanced Quote Email Interface -->
frontend/src/modules/quotes/components/QuoteEmailSender.vue
frontend/src/modules/quotes/components/EmailQuoteButton.vue
```

**Implementation Timeline:** 1 week

---

### **8. ACCOUNT MANAGER TRIP SORTING (Medium Priority)**

**Current Issue:** Account managers need to see their assigned trips first
**Implementation Required:**
- Filter pilgrimages by assigned account manager
- Default view shows assigned trips first
- Sort by assignment priority

**Implementation Required:**
```vue
<!-- Trip Assignment Filtering -->
frontend/src/modules/pilgrimages/components/AssignedTripsFilter.vue
frontend/src/modules/pilgrimages/services/tripAssignment.js
```

**Implementation Timeline:** 1-2 weeks

---

### **9. TASKS TAB INTEGRATIONS (NEW REQUEST - Out of Scope)**

**Current Issue:** Integrate calendar reminders and MS Office with AT&T
**Requirements:**
- Calendar reminder integration
- MS Office integration
- Meeting invitations for individuals & groups

**Implementation Required:**
```vue
<!-- Task Calendar Integration -->
frontend/src/modules/tasks/
├── components/CalendarIntegration.vue
├── components/MeetingScheduler.vue
├── components/MSOfficeIntegration.vue
└── services/calendarApi.js

backend/integrations/
├── microsoft_graph.py
├── calendar_sync.py
└── meeting_api.py
```

**Note:** This is outside original agreement scope
**Implementation Timeline:** 4-6 weeks (separate project)

---

### **10. EMPLOYEE EMAIL INTEGRATION (Critical Priority)**

**Current Issue:** Emails send from app email instead of employee's work email
**Requirements:**
- Configure SMTP for each employee's work email
- Customer replies go to employee, not app
- Maintain email thread continuity

**Implementation Required:**
```python
# Backend Email Configuration
backend/emails/services/employee_smtp.py
backend/users/models.py  # Add employee email settings
backend/emails/tasks.py  # Update email sending logic
```

**Implementation Timeline:** 2-3 weeks

---

### **11. DETAILED PAYMENT REPORTING (High Priority)**

**Current Issue:** Bulk bookings showing as one person instead of individual travelers
**Requirements:**
- Accurate traveler count reporting
- Individual passenger tracking in group bookings
- Detailed payment analytics per person

**Implementation Required:**
```vue
<!-- Enhanced Reporting System -->
frontend/src/modules/reports/
├── pages/PaymentReporting.vue
├── components/TravelerAnalytics.vue
├── components/GroupBookingBreakdown.vue
└── services/reportingApi.js

backend/reports/
├── models.py (TravelerTracking, PaymentAnalytics)
├── views.py (Enhanced reporting endpoints)
└── services/analytics.py
```

**Implementation Timeline:** 3-4 weeks

---

### **12. DOCUSIGN INTEGRATION (Critical Priority)**

**Current Issue:** Need DocuSign signature integration for terms & conditions and payment
**Requirements:**
- Pre-registration form with DocuSign
- Terms & conditions signature
- Payment authorization signature

**Implementation Required:**
```vue
<!-- DocuSign Integration -->
frontend/src/modules/docusign/
├── pages/DocumentSigning.vue
├── components/TermsConditionsSignature.vue
├── components/PaymentAuthorizationSignature.vue
└── services/docusignApi.js

backend/docusign/
├── models.py (SignatureTracking)
├── views.py (DocuSign webhook handlers)
└── services/docusign_service.py
```

**Implementation Timeline:** 3-4 weeks

---

## 📋 **IMPLEMENTATION PRIORITY MATRIX**

### **Phase 1 (Immediate - 4-6 weeks)**
1. **FTP Details System** (Critical for operations)
2. **Employee Email Integration** (Critical for communication)
3. **Automated Emails Enhancement** (Critical for customer experience)
4. **Sales Email Quote Tab Fix** (Quick win)

### **Phase 2 (Medium Term - 6-8 weeks)**
5. **Mobile/Tablet Responsiveness** (User experience)
6. **Automated Reminders System** (Operational efficiency)
7. **Manual Email Sending** (Account manager tools)
8. **DocuSign Integration** (Legal compliance)

### **Phase 3 (Long Term - 8-12 weeks)**
9. **Detailed Payment Reporting** (Analytics improvement)
10. **Airline-Specific Excel Lists** (Operational enhancement)
11. **Landing Page Redesign** (Marketing improvement)
12. **Account Manager Trip Sorting** (UI improvement)

### **Separate Project**
- **Tasks Tab Integration** (New scope - separate agreement needed)

---

## 🎯 **CRITICAL SUCCESS FACTORS**

### **Email System Requirements:**
- ✅ **ALL emails must send from account manager emails**
- ✅ **NO emails from app general email** (except specific reminders)
- ✅ **Customer replies go to account managers**
- ✅ **Email thread continuity maintained**

### **Technical Architecture:**
- Mobile-first responsive design
- Real-time email tracking and status
- Automated scheduling with manual override capability
- Integration with existing quote/pilgrimage workflow

### **User Experience:**
- Intuitive interface for account managers
- Clear email status indicators
- Easy manual override capabilities
- Comprehensive reporting and tracking

---

## 💰 **ESTIMATED DEVELOPMENT EFFORT**

| Phase | Features | Timeline | Complexity |
|-------|----------|----------|------------|
| Phase 1 | Critical Features (4 items) | 4-6 weeks | High |
| Phase 2 | Medium Priority (4 items) | 6-8 weeks | Medium |
| Phase 3 | Enhancement Features (4 items) | 8-12 weeks | Medium |
| **Total** | **12 Features** | **18-26 weeks** | **Mixed** |

**Note:** Tasks Tab Integration would require separate 4-6 week project

This roadmap prioritizes the most critical operational requirements while building toward a comprehensive, modern CRM system that meets all your pilgrimage management needs.
