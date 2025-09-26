{{ ... }}
    def test_get_default_output_name_removes_existing_date_suffix(self) -> None:
        """If source name already has _YYYY_MM_DD, ensure it's replaced (not duplicated)."""
        # Create temporary directory and file with existing date suffix
        temp_dir = tempfile.mkdtemp()
        existing_date = datetime.now().strftime("%Y_%m_%d")
        filename_with_date = f"sample_00_{existing_date}.txt"
        test_file_path = os.path.join(temp_dir, filename_with_date)
        
        try:
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write('test content')
            
            # Set source file
            self.processor.set_source_file(test_file_path)
            
            # Advance no time, but call to generate name should not duplicate suffix
            output_name = self.processor.get_default_output_name()
            
            # Expect exactly the same base (without the old date) plus today's date once
            expected_today = datetime.now().strftime("%Y_%m_%d")
            expected_output = f"sample_00_{expected_today}.txt"
            
            self.assertEqual(output_name, expected_output)
            # Also verify only one date pattern occurs
            import re as _re
            self.assertEqual(len(_re.findall(r"_\d{4}_\d{2}_\d{2}", output_name)), 1)
        finally:
            os.unlink(test_file_path)
            os.rmdir(temp_dir)
{{ ... }}
