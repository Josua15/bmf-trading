from django.shortcuts import redirect
from django.contrib import messages
from ..models import BmfBtcUsdtDaily, BmfEthUsdtDaily, BmfXrpUsdtDaily, BmfSolUsdtDaily, BmfDogeUsdtDaily  # Import all models
import openpyxl

# Map file types to their corresponding models and dynamic fields
MODEL_MAP = {
    'btc': {'model': BmfBtcUsdtDaily, 'volume_field': 'volume_btc'},
    'eth': {'model': BmfEthUsdtDaily, 'volume_field': 'volume_eth'},
    'xrp': {'model': BmfXrpUsdtDaily, 'volume_field': 'volume_xrp'},
    'sol': {'model': BmfSolUsdtDaily, 'volume_field': 'volume_sol'},
    'doge': {'model': BmfDogeUsdtDaily, 'volume_field': 'volume_doge'},
}

def home_view_logic(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        file_type = request.POST.get('file_type')  # Get the file type from the form
        excel_file = request.FILES['excel_file']

        # Validate the file type
        if file_type not in MODEL_MAP:
            messages.error(request, "Invalid file type selected.")
            return redirect('home')

        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, "Invalid file format. Please upload an .xlsx file.")
            return redirect('home')

        try:
            # Get the appropriate model and volume field based on file type
            model_info = MODEL_MAP[file_type]
            model = model_info['model']
            volume_field = model_info['volume_field']

            # Process the Excel file
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            records = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if all(row):  # Skip rows with missing data
                    # Dynamically create the record with the correct volume field
                    record_data = {
                        'unix': row[0],
                        'date': row[1],
                        'symbol': row[2],
                        'open': row[3],
                        'high': row[4],
                        'low': row[5],
                        'close': row[6],
                        volume_field: row[7],  # Dynamically assign the volume field
                        'volume_usdt': row[8],
                        'trade_count': row[9],
                    }
                    record = model(**record_data)
                    records.append(record)

            # Bulk insert records into the selected table
            model.objects.bulk_create(records)

            messages.success(request, f"Successfully uploaded {len(records)} records to the {file_type.upper()} table!")
        except Exception as e:
            messages.error(request, f"Error processing the file: {e}")

        return redirect('home')

    return None
