The `Prompts` section of the `Workspace` within Open WebUI enables users to create, manage, and share custom prompts. This feature streamlines interactions with AI models by allowing users to save frequently used prompts and easily access them through slash commands.

### Prompt Management

The Prompts interface provides several key features for managing your custom prompts:

* **Create**: Design new prompts with customizable titles, access levels, and content.
* **Share**: Share prompts with other users based on configured access permissions.
* **Access Control**: Set visibility and usage permissions for each prompt (refer to [Permissions](../rbac/permissions.md) for more details).
* **Slash Commands**: Quickly access prompts using custom slash commands during chat sessions.

### Creating and Editing Prompts

When creating or editing a prompt, you can configure the following settings:

* **Title**: Give your prompt a descriptive name for easy identification.
* **Access**: Set the access level to control who can view and use the prompt.
* **Command**: Define a slash command that will trigger the prompt (e.g., `/summarize`).
* **Prompt Content**: Write the actual prompt text that will be sent to the model.

### Prompt Variables

Open WebUI supports two kinds of variables to make your prompts more dynamic and powerful: **System Variables** and **Custom Input Variables**.

**System Variables** are automatically replaced with their corresponding value when the prompt is used. They are useful for inserting dynamic information like the current date or user details.

* **Clipboard Content**: Use `` to insert content from your clipboard.
* **Date and Time**:
  * ``: Current date
  * ``: Current date and time
  * ``: Current time
  * ``: Current timezone
  * ``: Current day of the week
* **User Information**:
  * ``: Current user's name
  * ``: User's selected language
  * ``: User's location (requires HTTPS and Settings > Interface toggle)

**Custom Input Variables** transform your prompts into interactive templates. When you use a prompt containing these variables, a modal window will automatically appear, allowing you to fill in your values. This is extremely powerful for creating complex, reusable prompts that function like forms. See the guidelines below for a full explanation.

By leveraging custom input variables, you can move beyond static text and build interactive tools directly within the chat interface. This feature is designed to be foolproof, enabling even non-technical users to execute complex, multi-step prompts with ease. Instead of manually editing a large block of text, users are presented with a clean, structured form. This not only streamlines the workflow but also reduces errors by guiding the user to provide exactly the right information in the right format. It unlocks a new level of interactive prompt design, making sophisticated AI usage accessible to everyone.

### Variable Usage Guidelines

* Enclose all variables with double curly braces: ``
* **All custom input variables are optional by default** - users can leave fields blank when filling out the form
* Use the `:required` flag to make specific variables mandatory when necessary
* The `` system variable requires:
  * A secure HTTPS connection
  * Enabling the feature in `Settings` > `Interface`
* The `` system variable requires clipboard access permission from your device

---

#### Using Custom Input Variables

**How It Works**

1. **Create a prompt** with one or more custom variables using the syntax below.
2. **Use the prompt's slash command** in the chat input.
3. An **"Input Variables" popup window** will appear with a form field for each variable you defined.
4. **Fill out the form** and click `Save`. Note that by default, all fields are optional unless explicitly marked as required.
5. The variables in your prompt will be replaced with your input, and the final prompt will be sent to the model.

**Syntax**

There are two ways to define a custom variable:

1. **Simple Input**: ``
    * This creates a standard, single-line `text` type input field in the popup window.
    * The field will be optional by default.

2. **Typed Input**: ``
    * This allows you to specify the type of input field (e.g., a dropdown, a date picker) and configure its properties.
    * The field will be optional by default unless you add the `:required` flag.

**Required vs Optional Variables**

By default, all custom input variables are **optional**, meaning users can leave them blank when filling out the form. This flexible approach allows for versatile prompt templates where some information might not always be needed.

To make a variable **required** (mandatory), add the `:required` flag:

```txt

```

When a field is marked as required:

* The form will display a visual indicator (asterisk) next to the field label
* Users cannot submit the form without providing a value
* Browser validation will prevent form submission if required fields are empty

**Input Types Overview**

You can specify different input types to build rich, user-friendly forms. Here is a table of available types and their properties.

| Type | Description | Available Properties | Syntax Example |
| :--- | :--- | :--- | :--- |
| **text** | A standard single-line text input field, perfect for capturing short pieces of information like names, titles, or single-sentence summaries. This is the **default type if no other is specified**. | `placeholder`, `default`, `required` | `` |
| **textarea**| A multi-line text area designed for capturing longer blocks of text, such as detailed descriptions, article content, or code snippets. | `placeholder`, `default`, `required` | `` |
| **select** | A dropdown menu that presents a predefined list of choices. This is ideal for ensuring consistent input for things like status, priority, or categories. | `options` (JSON array), `placeholder`, `default`, `required` | `` |
| **number** | An input field that is restricted to numerical values only. Useful for quantities, ratings, or any other numeric data. | `placeholder`, `min`, `max`, `step`, `default`, `required` | `` |
| **checkbox**| A simple checkbox that represents a true or false (boolean) value. It's perfect for on/off toggles, like 'Include a conclusion?' or 'Mark as urgent?'. | `label`, `default` (boolean), `required` | `` |
| **date** | A calendar-based date picker that allows users to easily select a specific day, month, and year, ensuring a standardized date format. | `placeholder`, `default` (YYYY-MM-DD), `required` | `` |
| **datetime-local**| A specialized picker that allows users to select both a specific date and a specific time. Great for scheduling appointments or logging event timestamps. | `placeholder`, `default`, `required` | `` |
| **color** | A visual color picker that allows the user to select a color or input a standard hex code (e.g., #FF5733). Useful for design and branding prompts. | `default` (hex code), `required` | `` |
| **email** | An input field specifically formatted and validated for email addresses, ensuring the user provides a correctly structured email. | `placeholder`, `default`, `required` | `` |
| **month** | A picker that allows users to select a specific month and year, without needing to choose a day. Useful for billing cycles, reports, or timelines. **Note:** This input type is only natively supported in Chrome and Edge. In Firefox and Safari, it will display as a plain text input instead of a month picker. | `placeholder`, `default`, `required` | `` |
| **range** | A slider control that allows the user to select a numerical value from within a defined minimum and maximum range. Ideal for satisfaction scores or percentage adjustments. | `min`, `max`, `step`, `default`, `required` | `` |
| **tel** | An input field designed for telephone numbers. It semantically indicates the expected input type for browsers and devices. | `placeholder`, `default`, `required` | `` |
| **time** | A picker for selecting a time. Useful for scheduling meetings, logging events, or setting reminders without an associated date. | `placeholder`, `default`, `required` | `` |
| **url** | An input field for web addresses (URLs). It helps ensure that the user provides a link, which can be useful for prompts that analyze websites or reference online sources. | `placeholder`, `default`, `required` | `` |
| **map** | **(Experimental)** An interactive map interface that lets users click to select geographic coordinates. This is a powerful tool for location-based prompts. | `default` (e.g., "51.5,-0.09"), `required` | `` |

#### Example Use Cases

**1. Flexible Article Summarizer**

Create a reusable prompt where the article content is required but additional parameters are optional.

* **Command:** `/summarize_article`
* **Prompt Content:**

    ```txt
    Please summarize the following article. 

    

    

    
    ```

    When you type `/summarize_article`, a modal will appear with a required text area for the article, and optional fields for customizing the summary style.

**2. Advanced Bug Report Generator**

This prompt ensures critical information is captured while allowing optional details.

* **Command:** `/bug_report`
* **Prompt Content:**

    ```txt
    Generate a bug report with the following details:

    **Summary:** 
    **Priority:** 
    **Steps to Reproduce:**
    

    **Additional Context:** 
    **Workaround:** 

    Please format this into a clear and complete bug report document.
    ```

    This creates a form where title, priority, and steps are mandatory, but additional context and workarounds are optional.

**3. Social Media Post Generator with Smart Defaults**

This prompt generates tailored content with required core information and optional customizations.

* **Command:** `/social_post`
* **Prompt Content:**

    ```txt
    Generate a social media post for .

    **Topic:** 
    **Key Message:** 
    **Tone of Voice:** 
    **Call to Action:** 
    **Character Limit:** 
    **Include Hashtags:** 

    Please create an engaging post optimized for the selected platform.
    ```

**4. Meeting Minutes Assistant with Flexible Structure**

Generate structured meeting minutes with required basics and optional details.

* **Command:** `/meeting_minutes`
* **Prompt Content:**

    ```txt
    # Meeting Minutes

    **Date:** 
    **Time:** 
    **Meeting Title:** 
    **Attendees:** 

    ## Agenda / Key Discussion Points
    

    ## Decisions Made
    

    ## Action Items
    

    ## Next Meeting
    **Date:** 
    **Topics:** 

    Please format the above information into a clean and professional meeting summary.
    ```

**5. Content Review Template**

A flexible template for reviewing various types of content.

* **Command:** `/content_review`
* **Prompt Content:**

    ```txt
    Please review the following :

    **Content Title:** 
    **Content:** 

    **Review Focus:** 
    **Target Audience:** 
    **Specific Concerns:** 
    **Word Count Target:** 

    Please provide detailed feedback and suggestions for improvement.
    ```

### Access Control and Permissions

Prompt management is controlled by the following permission settings:

* **Prompts Access**: Users need the `USER_PERMISSIONS_WORKSPACE_PROMPTS_ACCESS` permission to create and manage prompts.
* For detailed information about configuring permissions, refer to the [Permissions documentation](../rbac/permissions.md).

### Best Practices

* Use clear, descriptive titles for your prompts
* Create intuitive slash commands that reflect the prompt's purpose
* **Design with flexibility in mind**: Mark only truly essential fields as required, leaving optional fields for enhanced customization
* For custom variables, use clear names (e.g., `` instead of ``) and descriptive `placeholder` text to make templates easy to understand
* **Provide sensible defaults** for optional fields where appropriate to speed up form completion
* **Use the required flag strategically** - only require information that is absolutely necessary for the prompt to function properly
* Document any specific requirements or expected inputs in the prompt description
* Test prompts with different variable combinations, including scenarios where optional fields are left blank
* Consider access levels carefully when sharing prompts with other users - public sharing means that it will appear automatically for all users when they hit `/` in a chat, so you want to avoid creating too many
* **Consider user workflows**: Think about which information users will always have versus what they might want to customize occasionally

### Migration Notes

If you have existing prompts created before this update, they will continue to work as before. However, note that:

* All existing variables are now treated as optional by default
* If you want to maintain required behavior for critical fields, edit your prompts to add the `:required` flag to those variables
* This change provides better user experience by allowing flexible usage of prompt templates
