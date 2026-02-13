# PawPal+ Project Reflection

## 1. System Design
- The 3 core actions a user should be able to perform are allowing the user to enter basic information, allowing the user to add and edit tasks, and allowing the user to generate a daily plan based off the contraints they have.
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The PawPal+ system consists of four main classes:

Owner - Represents the pet owner with time constraints and preferences. Responsibilities include managing a collection of pets, tracking available time (in minutes), and storing user preferences for scheduling. Acts as the primary user entity in the system.

Pet - Represents an individual pet with basic information and care needs. Responsibilities include storing pet details (name, species, age) and managing a list of special needs that affect care requirements. Implemented as a dataclass for simplicity.

Task - Represents a care activity with scheduling metadata. Responsibilities include storing task details (name, duration, category), maintaining priority levels (1-5), and indicating whether the task is required. Supports comparison operations for priority-based sorting. Implemented as a dataclass and optionally linked to a specific pet.

Scheduler - The central coordinator that connects all components. Responsibilities include managing the owner's schedule, organizing tasks based on priority and time constraints, and generating an optimized daily care plan that respects the owner's available minutes and pet needs.

Key relationships: Owner owns multiple Pets (1-to-many), and Scheduler uses Owner, Pets, and Tasks to create scheduling plans.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, several design changes were made during implementation to address critical relationship and logic bottlenecks:

1. **Added Bidirectional Owner-Pet Relationship**: Initially, the Pet class had no reference back to its Owner. I added an `owner` field to Pet so that a pet can identify which owner it belongs to. This enables validation (e.g., preventing tasks for pets the owner doesn't have) and allows direct pet-to-owner navigation.

2. **Added Bidirectional Task-Pet Tracking**: The original design allowed Task to reference Pet, but Pet had no way to access its tasks. I added a `tasks` field to Pet, creating a bidirectional association. This allows querying "what tasks are associated with this pet?" which is essential for care planning and pet-specific task management.

3. **Removed Redundant Scheduler.pets**: Initially, Scheduler maintained its own `self.pets` list separate from `self.owner.pets`. This created data consistency issues. I removed the redundant list and now Scheduler accesses pets through `self.owner.pets`, establishing a single source of truth.

4. **Two-Pass Scheduling Algorithm**: The initial generate_daily_plan() stub gave no guidance on implementation. I implemented a constraint-aware two-pass algorithm: first schedule all required tasks (with validation that they fit), then greedily add optional tasks by priority. This ensures feasibility and prevents over-scheduling.

5. **Enhanced Validation**: Added pet ownership validation in `add_task()` to prevent orphaned tasks, and priority range validation in `set_priority()` to prevent invalid states.

These changes were made because the original design had information asymmetry and lacked constraint enforcement, which would cause runtime errors or impossible schedules. The bidirectional relationships create a more robust model that prevents invalid states at insertion time rather than discovery time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
