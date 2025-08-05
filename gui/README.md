# SecWiz GUI Package

This package contains the GUI interface and backend integration for SecWiz.

## 📁 Structure

```
gui/
├── __init__.py              # Package initialization
├── gui.py                   # Main GUI interface (CustomTkinter)
├── backend_integration.py   # Backend integration layer
├── requirements.txt         # GUI-specific dependencies
└── README.md               # This file
```

## 🚀 Features

### GUI Interface (`gui.py`)
- **Modern CustomTkinter Interface**: Dark theme with blue accents
- **Multi-Panel Layout**: Left panel for configuration, right panel for results
- **Dynamic Tab System**: Different tabs based on scan type
- **Real-time Progress Updates**: Live status updates during scans
- **Professional Design**: Inspired by Burp Suite and Postman

### Backend Integration (`backend_integration.py`)
- **Tool Integration**: Bridges GUI with existing scanner tools
- **Progress Callbacks**: Real-time progress updates to GUI
- **Error Handling**: Comprehensive error handling and reporting
- **Result Formatting**: Structured results for GUI display

## 🎯 Scan Types

### Full Scan
- Port scanning
- Directory enumeration
- Form input extraction
- SQL injection testing

### Port Scan
- All ports analysis
- Open ports with services
- Service detection

### Directory Scan
- All files discovered
- Accessible files
- Protected files

## 🔧 Usage

### Running the GUI
```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

### Testing Integration
```bash
# Run integration tests
python test_integration.py
```

## 📋 Dependencies

### GUI Dependencies
- `customtkinter>=5.2.0` - Modern GUI framework
- `Pillow>=9.5.0` - Image processing for assets
- `requests>=2.31.0` - HTTP requests
- `beautifulsoup4>=4.12.0` - HTML parsing
- `lxml>=4.9.0` - XML/HTML processing

### External Tools Required
- `gobuster` - Directory enumeration
- `sqlmap` - SQL injection testing

## 🎨 Color Scheme

The GUI uses a professional blue theme:
- **Primary**: `#2196F3` (Blue)
- **Secondary**: `#1976D2` (Darker blue)
- **Accent**: `#64B5F6` (Light blue)
- **Success**: `#4CAF50` (Green for success states)
- **Warning**: `#FF9800` (Orange for warnings)
- **Error**: `#f44336` (Red for errors)

## 🔄 Integration Flow

1. **User Input**: Target domain and scan type selection
2. **Backend Processing**: Integration layer calls appropriate tools
3. **Progress Updates**: Real-time status updates to GUI
4. **Result Display**: Formatted results shown in appropriate tabs
5. **Report Generation**: Export results to files

## 🛠️ Development

### Adding New Scan Types
1. Update `tab_configs` and `tab_names` in `gui.py`
2. Add corresponding method in `backend_integration.py`
3. Update `get_tab_content()` method for new content formatting

### Modifying Backend Tools
1. Update the integration methods in `backend_integration.py`
2. Ensure proper error handling and progress callbacks
3. Test with the integration test suite

## 📊 Testing

Run the test suite to verify integration:
```bash
python test_integration.py
```

This will test:
- ✅ Import functionality
- ✅ Backend integration
- ✅ GUI creation
- ✅ Module connectivity

## 🎯 Next Steps

1. **Enhanced Error Handling**: More detailed error messages
2. **Progress Bars**: Visual progress indicators
3. **Report Export**: PDF and HTML report generation
4. **Configuration Management**: Save/load scan configurations
5. **Plugin System**: Extensible tool integration

## 📝 Notes

- The GUI is designed to be non-blocking during scans
- All backend operations run in separate threads
- Results are cached and displayed in real-time
- The integration layer provides a clean API for tool communication 