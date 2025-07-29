# String Replacer Application - Task Specification

## Original Requirements

Create a simple tkinter project with the following specifications:

### Core Features Required

1. **File Selection**
   - Button to select a file for processing
   - Display selected file path

2. **Find and Replace Functionality**
   - Input field for "find" text (e.g., "foo")
   - Input field for "replace" text (e.g., "bar")
   - Process text replacement in selected file

3. **Random String Generation**
   - Generate random strings as replacement text
   - Button to specify maximum number of characters for random string
   - Button to generate random string with specified length

4. **Output File Management**
   - Button/field to choose name of new file with replaced strings
   - Keep existing file unchanged
   - Create a copy with updated strings

### Technical Requirements

- **Framework**: tkinter (Python's standard GUI library)
- **File Safety**: Original files must remain unchanged
- **User Interface**: Simple, intuitive GUI with buttons and input fields

## Enhanced Requirements (Applied)

Based on software engineering best practices, the following enhancements were implemented:

### Architecture Requirements

1. **Object-Oriented Programming (OOP)**
   - All components structured as classes
   - Proper encapsulation and method organization
   - Clear object responsibilities

2. **Standard Python Package Structure**
   - Organized folder/file layout
   - Proper module imports and __init__.py files
   - Separation of source code and tests

3. **MVC Architecture**
   - Model: Business logic and data management
   - View: GUI components and user interface
   - Controller: Coordination between Model and View

### Testing Requirements

4. **Comprehensive Unit Tests**
   - Tests for all Model, View, and Controller components
   - Edge case and error condition testing
   - Integration tests for complete workflows

5. **Documentation**
   - PLANNING.md: Architecture and design decisions
   - TASK.md: Requirements and specifications
   - README.md: User guide and setup instructions

## Functional Specifications

### User Workflow

1. **File Selection Process**
   ```
   User clicks "Browse" → File dialog opens → User selects file → 
   File path displayed → Default output name generated
   ```

2. **Text Replacement Process**
   ```
   User enters find text → User enters replace text OR generates random string →
   User specifies output filename → User clicks "Process File" →
   New file created with replacements
   ```

3. **Random String Generation**
   ```
   User sets desired length → User clicks "Generate Random String" →
   Random string appears in replace field → Ready for processing
   ```

### Input Validation

- **File Selection**: Must be valid, existing file
- **Output Name**: Must be specified and valid filename
- **Random Length**: Must be positive integer
- **Find/Replace**: At least one operation must be specified

### Error Handling

- **File Not Found**: Clear error message with retry option
- **Permission Errors**: Informative message about file access
- **Invalid Input**: Specific guidance on correct input format
- **Processing Errors**: Safe failure with original file preserved

## Technical Implementation Details

### Model Layer (FileProcessor)

**Responsibilities:**
- File reading and writing operations
- String replacement logic
- Random string generation
- Input validation and error handling
- State management for processing parameters

**Key Methods:**
- `set_source_file(path)`: Validate and set source file
- `set_find_replace_text(find, replace)`: Set replacement parameters
- `generate_random_string(length)`: Create random alphanumeric string
- `process_file()`: Execute find/replace and create output file
- `get_default_output_name()`: Generate default output filename

### View Layer (MainView)

**Responsibilities:**
- Create and manage GUI widgets
- Handle user input collection
- Display status messages and dialogs
- Provide interface for controller communication

**Key Components:**
- File selection widgets (entry, browse button)
- Find/replace input fields
- Random string generation controls
- Output filename specification
- Process and clear action buttons
- Status display area

### Controller Layer (MainController)

**Responsibilities:**
- Coordinate between Model and View
- Handle user action events
- Manage error handling and user feedback
- Orchestrate business logic flow

**Key Methods:**
- `browse_file()`: Handle file selection workflow
- `generate_random_string()`: Manage random string generation
- `process_file()`: Coordinate file processing workflow
- `clear_all()`: Reset application state

## Quality Assurance Requirements

### Testing Coverage

1. **Unit Tests**
   - Model: All business logic methods
   - View: GUI component behavior
   - Controller: Event handling and coordination

2. **Integration Tests**
   - Complete user workflows
   - MVC component interactions
   - Error handling across layers

3. **Test Categories**
   - Happy path scenarios
   - Error conditions
   - Edge cases
   - Input validation

### Code Quality Standards

- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Graceful failure with user feedback
- **Code Organization**: Clear separation of concerns
- **Maintainability**: Modular, extensible design

## Success Criteria

### Functional Success
- ✅ All original requirements implemented
- ✅ File processing works correctly
- ✅ Random string generation functional
- ✅ Safe file operations (originals preserved)
- ✅ Intuitive user interface

### Technical Success
- ✅ MVC architecture properly implemented
- ✅ OOP principles applied throughout
- ✅ Standard Python package structure
- ✅ Comprehensive test coverage
- ✅ Clean, maintainable codebase

### User Experience Success
- ✅ Responsive, intuitive GUI
- ✅ Clear status feedback
- ✅ Helpful error messages
- ✅ Smooth workflow from file selection to processing

## Deliverables

### Core Application Files
- `main.py`: Application entry point
- `src/models/file_processor.py`: Business logic
- `src/views/main_view.py`: GUI interface
- `src/controllers/main_controller.py`: Application coordination

### Testing Suite
- `tests/test_file_processor.py`: Model unit tests
- `tests/test_main_view.py`: View unit tests
- `tests/test_main_controller.py`: Controller unit tests
- `tests/test_integration.py`: Integration tests
- `tests/run_tests.py`: Test runner script

### Documentation
- `README.md`: User guide and setup instructions
- `PLANNING.md`: Architecture and design documentation
- `TASK.md`: This requirements specification
- `requirements.txt`: Dependency specification

## Usage Instructions

### Running the Application
```bash
python main.py
```

### Running Tests
```bash
python tests/run_tests.py
```

### Basic Usage Flow
1. Launch application
2. Click "Browse" to select input file
3. Enter text to find and replace
4. Optionally generate random replacement string
5. Specify output filename
6. Click "Process File"
7. Verify new file created with replacements

## Task Completion Log

### ✅ Completed Tasks

#### 2025-07-28: .windsurf/rules.md Compliance Update
- **Status**: COMPLETED
- **Description**: Updated entire codebase to comply with .windsurf/rules.md requirements
- **Changes Made**:
  - Added type hints to all functions across all modules
  - Updated all docstrings to Google-style format with Args/Returns sections
  - Added pydantic for data validation in FileProcessor model
  - Updated requirements.txt to include pydantic>=1.10.0
  - Added comprehensive # Reason: comments for complex logic
  - Updated README.md to reflect new dependencies and compliance
  - Ensured all files are under 500 lines (compliance verified)
  - Maintained PEP8 formatting standards
- **Files Modified**:
  - `src/models/file_processor.py`: Added pydantic validation, type hints, Google docstrings
  - `src/views/main_view.py`: Added type hints and Google docstrings
  - `src/controllers/main_controller.py`: Added type hints and Google docstrings
  - `main.py`: Added type hints and Google docstrings
  - `requirements.txt`: Added pydantic dependency
  - `README.md`: Updated architecture section and requirements
  - `TASK.md`: Added this completion log

#### 2025-07-28: Enhanced Random String Generation with Character Set Selection
- **Status**: COMPLETED
- **Description**: Added checkbox functionality to customize random string character sets
- **New Features**:
  - Added three checkboxes: UC (uppercase), lc (lowercase), number
  - Users can select any combination of character types
  - Random strings generated based on selected character sets only
  - Validation ensures at least one character type is selected
  - Clear status messages showing which character types were used
  - Checkboxes reset to default (all checked) when clearing fields
- **Technical Implementation**:
  - Enhanced `FileProcessor.generate_random_string()` with character set parameters
  - Added checkbox UI components in random string section
  - Updated controller to handle checkbox states and validation
  - Added getter methods for checkbox states in view
  - Comprehensive error handling for invalid selections
- **Files Modified**:
  - `src/models/file_processor.py`: Enhanced random string generation with character set options
  - `src/views/main_view.py`: Added checkbox UI components and getter methods
  - `src/controllers/main_controller.py`: Updated to handle character set selection logic
  - `TASK.md`: Added this completion log

#### 2025-07-28: Date-Based Output File Naming
- **Status**: COMPLETED
- **Description**: Changed output file naming from `_updated` suffix to `_yyyy_mm_dd` format using today's date
- **Enhancement Details**:
  - Modified `get_default_output_name()` method to use current date
  - Format: `sample_00.txt` → `sample_00_2025_07_28.txt`
  - Uses `datetime.now().strftime("%Y_%m_%d")` for consistent formatting
  - Works with all file extensions (.txt, .sql, .json, etc.)
  - Handles files without extensions correctly
  - Maintains original filename structure with date suffix
- **Technical Implementation**:
  - Added `datetime` import to FileProcessor model
  - Updated docstring to reflect new behavior
  - Comprehensive unit tests with 8 test cases covering:
    - Current date inclusion
    - Different file extensions
    - Specific example verification
    - Mocked date testing
    - Complex filenames
    - Edge cases (no extension, no source file)
    - Date format consistency
- **Files Modified**:
  - `src/models/file_processor.py`: Updated `get_default_output_name()` method
  - `tests/test_date_based_naming.py`: Created comprehensive unit tests
  - `TASK.md`: Added this completion log

## Conclusion

This task specification documents the complete requirements and implementation details for the String Replacer application. The project successfully demonstrates modern software engineering practices while delivering a functional, user-friendly file processing tool.

The codebase now fully complies with `.windsurf/rules.md` standards including type hints, Google-style docstrings, pydantic validation, and comprehensive documentation.
