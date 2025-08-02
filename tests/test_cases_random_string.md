# Test Cases for Random String Generation Function

## Overview
This document outlines comprehensive test cases for the `generate_random_string()` function in `file_processor.py`, considering various scenarios with file selection and DB file checkbox interactions.

## Function Under Test
- **Function**: `FileProcessor.generate_random_string()`
- **Location**: `src/models/file_processor.py`
- **Parameters**:
  - `length: Optional[int] = None` (uses `max_random_length` if None)
  - `use_uppercase: bool = True`
  - `use_lowercase: bool = True` 
  - `use_numbers: bool = True`

## Test Categories

### 1. Basic Function Tests (No File Context)

#### Test 1.1: Default Parameters
- **Input**: `generate_random_string()`
- **Expected**: String of length `max_random_length` (default 10) with uppercase, lowercase, and numbers
- **Validation**: 
  - Length equals `max_random_length`
  - Contains at least one uppercase letter
  - Contains at least one lowercase letter
  - Contains at least one number

#### Test 1.2: Custom Length
- **Input**: `generate_random_string(length=15)`
- **Expected**: String of length 15 with all character types
- **Validation**: Length equals 15

#### Test 1.3: Character Set Combinations
- **Test 1.3a**: Only uppercase
  - **Input**: `generate_random_string(use_lowercase=False, use_numbers=False)`
  - **Expected**: String with only uppercase letters (A-Z)
- **Test 1.3b**: Only lowercase
  - **Input**: `generate_random_string(use_uppercase=False, use_numbers=False)`
  - **Expected**: String with only lowercase letters (a-z)
- **Test 1.3c**: Only numbers
  - **Input**: `generate_random_string(use_uppercase=False, use_lowercase=False)`
  - **Expected**: String with only digits (0-9)
- **Test 1.3d**: Uppercase + Numbers
  - **Input**: `generate_random_string(use_lowercase=False)`
  - **Expected**: String with uppercase letters and numbers only

#### Test 1.4: Error Cases
- **Test 1.4a**: Zero length
  - **Input**: `generate_random_string(length=0)`
  - **Expected**: `ValueError: "Length must be a positive number"`
- **Test 1.4b**: Negative length
  - **Input**: `generate_random_string(length=-5)`
  - **Expected**: `ValueError: "Length must be a positive number"`
- **Test 1.4c**: No character sets
  - **Input**: `generate_random_string(use_uppercase=False, use_lowercase=False, use_numbers=False)`
  - **Expected**: `ValueError: "At least one character type must be selected"`

### 2. File Selection Context Tests

#### Test 2.1: Regular File Selected (No DB Checkbox)
- **Setup**: 
  - Select a regular text file (e.g., `document.txt`)
  - DB checkbox: UNCHECKED
- **Action**: Call `generate_random_string()` via UI or direct function call
- **Expected**: Function works normally with default parameters
- **Validation**: Generated string follows standard rules

#### Test 2.2: Regular File Selected (DB Checkbox Checked)
- **Setup**: 
  - Select a regular text file (e.g., `document.txt`)
  - DB checkbox: CHECKED
- **Action**: Process file using DB password functionality
- **Expected**: `generate_random_string()` called internally by `process_db_password_file()`
- **Validation**: 
  - New password generated with specified character sets
  - Length equals `max_random_length`

### 3. DB File Checkbox Interaction Tests

#### Test 3.1: DB Checkbox Checked BEFORE File Selection
- **Steps**:
  1. Check DB file checkbox
  2. Select a file with DB password patterns
- **Expected**: 
  - `process_db_password_file()` should be used
  - `generate_random_string()` called with DB-specific parameters
- **Validation**: Password replacement occurs correctly

#### Test 3.2: DB Checkbox Checked AFTER File Selection
- **Steps**:
  1. Select a file with DB password patterns
  2. Check DB file checkbox
- **Expected**: Same as Test 3.1
- **Validation**: Order shouldn't matter - same functionality

#### Test 3.3: DB Checkbox Unchecked BEFORE File Selection
- **Steps**:
  1. Ensure DB checkbox is unchecked
  2. Select any file
- **Expected**: Regular file processing (not DB password processing)
- **Validation**: `generate_random_string()` not called automatically

#### Test 3.4: DB Checkbox Unchecked AFTER File Selection
- **Steps**:
  1. Select a file
  2. Ensure DB checkbox is unchecked
- **Expected**: Same as Test 3.3
- **Validation**: Regular processing mode

### 4. File Type Specific Tests

#### Test 4.1: DB File with Valid Password Patterns
- **File Content**: First line contains `BY "oldpass"` and `REPLACE "currentpass"`
- **Setup**: DB checkbox checked
- **Expected**: 
  - `generate_random_string()` generates new password
  - Old patterns replaced with new random password
- **Validation**: 
  - New password has correct length and character sets
  - File content updated correctly

#### Test 4.2: DB File with Invalid Password Patterns
- **File Content**: First line missing required patterns
- **Setup**: DB checkbox checked
- **Expected**: `ValueError` about missing password patterns
- **Validation**: Error message is descriptive

#### Test 4.3: Non-DB File with DB Checkbox Checked
- **File Content**: Regular text file without password patterns
- **Setup**: DB checkbox checked
- **Expected**: `ValueError` about missing password patterns
- **Validation**: Function fails gracefully with clear error

### 5. Edge Cases and Integration Tests

#### Test 5.1: Very Large Random String
- **Input**: `generate_random_string(length=1000)`
- **Expected**: String of exactly 1000 characters
- **Validation**: Performance and memory usage acceptable

#### Test 5.2: Multiple Consecutive Calls
- **Action**: Call `generate_random_string()` 10 times with same parameters
- **Expected**: 10 different random strings
- **Validation**: No two strings should be identical

#### Test 5.3: File with Date Suffix + DB Processing
- **File**: `database_2024_07_15.sql` with password patterns
- **Setup**: DB checkbox checked
- **Expected**: 
  - Output file: `database_2025_08_01.sql` (today's date)
  - Random password generated and replaced
- **Validation**: Both date logic and password generation work together

### 6. UI Integration Tests

#### Test 6.1: Character Set Checkboxes in UI
- **Setup**: UI with checkboxes for uppercase, lowercase, numbers
- **Action**: Toggle different combinations
- **Expected**: `generate_random_string()` called with correct parameters
- **Validation**: Generated strings match checkbox selections

#### Test 6.2: Length Input Field
- **Setup**: UI field for specifying random string length
- **Action**: Enter different values (5, 10, 20, etc.)
- **Expected**: Generated strings have specified lengths
- **Validation**: Length validation works in UI

## Test Data Files

### Sample DB File (valid_db_file.sql)
```sql
ALTER USER 'admin'@'localhost' IDENTIFIED BY "newpass123" REPLACE "oldpass456";
SELECT * FROM users;
UPDATE settings SET value = 'active';
```

### Sample DB File (invalid_db_file.sql)
```sql
SELECT * FROM users;
UPDATE settings SET value = 'active';
-- Missing password patterns
```

### Sample Regular File (document.txt)
```
This is a regular text document.
It contains no database password patterns.
Just normal text content.
```

## User-Defined Cases (Case 1 & Case 2)

### Case 1: Generate Random String → Process File
- **Given**: 
  - Source file selected via Browse
  - Random string length selected
  - Generate Random String button pushed → `sel_file_new_pw = "12345"`
  - Any combination of UC/lc/number selected
  - File Type: DB pwd checkbox checked
- **When**: Click Process file
- **Then**: `sel_file_new_pw` ("12345") is written in contents of Output File

### Case 2: Existing Replace Text → Process File
- **Given**: 
  - EXACTLY all conditions in Case 1, EXCEPT do NOT push "Generate Random String" button
  - Random string IS STILL THE SAME as Case 1 = `sel_file_new_pw = "12345"` 
  - Value STILL APPEARS in "Replace With" box (hasn't been modified)
- **When**: Click Process file
- **Then**: The same `sel_file_new_pw` value ("12345") is written in contents of Output File

## Success Criteria
- All basic function tests pass
- File selection doesn't break random string generation
- DB checkbox state correctly influences function behavior
- Error cases are handled gracefully
- UI integration works seamlessly
- Performance is acceptable for reasonable input sizes
- **Case 1 works**: Generated random string is used in DB password processing
- **Case 2 works**: Existing replace text value is used in DB password processing

## Notes
- Test both programmatic calls and UI-triggered calls
- Verify that random strings are truly random (no patterns)
- Ensure character set restrictions are properly enforced
- Test with various file encodings if applicable
