# Spade SDK

Spade SDK provides basic classes to implement Spade Files and Processes.
For more information about Spade, please visit [Spade]()

It has no dependencies on other Python libraries, and allows development for Spade without
a need to install the full Spade app.

## Installation

```bash
pip install spadesdk
```

## Basic objects

### FileProcessor

`FileProcessor` processes the file uploaded by the user in the Spade app.

### Executor

`Executor` executes a Spade process, either by directly running Python code or by
calling an external service.

### HistoryProvider

`HistoryProvider` provides the history of a Spade from if the actual process is executed
by an external service. If the process is executed in Spade, a `HistoryProvider` is not
needed.
